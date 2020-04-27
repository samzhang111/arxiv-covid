import xml.etree.ElementTree as ET
import os
import sys
import glob

import pandas as pd


def clean_str(s):
    if s:
        return ' '.join(s.split())

    return ""


def get_contents(tag):
    return " ".join([clean_str(x) for x in tag.itertext()])


def get_str_if_exists(tag):
    if tag is None:
        return ""

    return clean_str(tag.text)


def parse_tree(tree):
    meta = tree.find("front").find("article-meta")

# parse id
    article_id_tags = meta.findall("article-id")
    article_ids = []
    for article_id in article_id_tags:
        id_type = article_id.get("pub-id-type")
        id_text = get_str_if_exists(article_id)

        article_ids.append({
            'id_type': id_type,
            'id': id_text
        })

# parse title
    title_group = meta.find("title-group")
    article_title = get_str_if_exists(title_group.find("article-title"))

# parse authors
    contrib_groups = meta.findall("contrib-group")
    contributors = []
    for contrib_group in contrib_groups:
        inst = ""
        aff = contrib_group.find("aff")
        if aff is not None:
            inst = get_str_if_exists(aff.find("institution"))

        contribs = contrib_group.findall("contrib")

        for contrib in contribs:
            contrib_type = contrib.get("contrib-type")
            corresp = contrib.get("corresp")

            contrib_id_tags = contrib.findall("contrib-id")
            contrib_ids = []
            for contrib_id in contrib_id_tags:
                contrib_id_type = contrib_id.get("contrib-id-type")
                contrib_id_text = get_str_if_exists(contrib_id)

                contrib_ids.append({
                    'type': contrib_id_type,
                    'content': contrib_id_text
                })

            name_tag = contrib.find("name")
            if name_tag is None:
                collab_tag = contrib.find("collab")
                if collab_tag is None:
                    continue

                # rare case where a non-human is collaborator, eg
                # https://www.biorxiv.org/content/10.1101/2020.01.07.897751v1
                contributors.append({
                    'surname': "",
                    'given_names': "",
                    'contrib_ids': contrib_ids,
                    'corresp': corresp,
                    'contrib_type': contrib_type,
                    'affiliation': get_str_if_exists(collab_tag)
                })
                continue

            surname = get_str_if_exists(name_tag.find("surname"))
            given_names = get_str_if_exists(name_tag.find("given-names"))

            contributors.append({
                'surname': surname,
                'given_names': given_names,
                'contrib_ids': contrib_ids,
                'corresp': corresp,
                'contrib_type': contrib_type,
                'affiliation': inst
            })

# author notes
    author_note_tags = meta.findall("author-notes")
    author_notes = []
    for author_note in author_note_tags:
        corresps = author_note.findall("corresp")
        for corresp in corresps:
            corresp_text = get_contents(corresp)
            email = get_str_if_exists(corresp.find("email"))
            author_notes.append({
                'email': email,
                'corresp_text': corresp_text
            })

# history
    history = meta.find("history")
    received = history.find(".//date[@date-type='received']")
    year_received = get_str_if_exists(received.find('year'))
    date_received = "{}-{}-{}".format(
        get_str_if_exists(received.find('year')),
        get_str_if_exists(received.find('month')),
        get_str_if_exists(received.find('day'))
    )

    article = {
        'title': article_title,
        'contributors': contributors,
        'corresp_texts': author_notes,
        'ids': article_ids,
        'date_received': date_received,
        'year_received': year_received
    }

    return article


def parse_file(fn):
    with open(fn) as f:
        xmlstr = f.read()

    tree = ET.fromstring(xmlstr)

    return parse_tree(tree)


def parse_directory(path):
    results = []
    results_authors = []
    for i, d in enumerate(glob.iglob(path + "/**/*.xml", recursive=True)):
        parsed = parse_file(d)
        results.append(parsed)
        auth_results = parsed['contributors']
        for auth in auth_results:
            auth['id'] = parsed['ids'][0]['id']
            auth['date_received'] = parsed['date_received']
            auth['year_received'] = parsed['year_received']

        results_authors.extend(auth_results)

        if i % 100 == 0:
            print('.', end='')
            sys.stdout.flush()

    df = pd.DataFrame(results)
    df.to_csv("./biorxiv-parsed.csv", index=False)

    df_authors = pd.DataFrame(results_authors)
    df_authors.to_csv("./biorxiv-parsed-authors.csv", index=False)


if __name__ == '__main__':
    import pprint

    if os.path.isdir(sys.argv[1]):
        parse_directory(sys.argv[1])
    elif os.path.isfile(sys.argv[1]):
        pprint.pprint(parse_file(sys.argv[1]))
    else:
        print("Need sys.argv[1] to be file or directory")
