# Global Imports
from pdftotext import PDF
from pathlib import Path
from json import dump
from typing import (List, Dict, Union)
# Local Imports
from config import (get_document_paths, _get_years)


def get_document(fp: Path):
    with fp.open("rb") as file:
        pdf = PDF(file)
    return pdf


def save_to_json(data, fp: Path):
    with fp.open("w+") as json_file:
        dump(data, json_file, ensure_ascii=False)


def get_abstract(data: List[str]) -> Union[Dict[str, List[str]], None]:
    start_abstract = None
    start_resumo = None
    end = None
    resumo_before_abstract = False
    for n, line in enumerate(data):
        if line.lower().startswith("abstract"):
            start_abstract = n
        elif line.lower().startswith("resumo"):
            start_resumo = n
            if not resumo_before_abstract and start_abstract == None:
                resumo_before_abstract = True
        elif line.lower().startswith("1.") and n != 0:
            end = n
    resp = dict()
    if end == None:
        return None
    elif start_resumo != None and start_abstract != None:
        if resumo_before_abstract:
            resumo = data[start_resumo:start_abstract]
            abstract = data[start_abstract:end]
        else:
            resumo = data[start_resumo:end]
            abstract = data[start_abstract:start_resumo]

        # Remove a palavra abstract do começo do texto
        abstract[0] = abstract[0][len("abstract") + 2:]
        resp["abstract"] = str().join(abstract)
        resumo[0] = resumo[0][len("resumo") + 2:]
        resp["resumo"] = str().join(resumo)

        return resp

    elif start_abstract != None:
        abstract = data[start_abstract:end]
        # Remove a palavra abstract do começo do texto
        abstract[0] = abstract[0][len("abstract") + 2:]
        resp["abstract"] = str().join(abstract)
        return resp
    elif start_resumo != None:
        resumo = data[start_resumo:end]
        resumo[0] = resumo[0][len("resumo") + 2:]
        resp["resumo"] = str().join(resumo)
        return resp

    return None


def extract_abstracts(pdf: PDF) -> List[List[str]]:
    page_lines = pdf_serializer(pdf)
    abstracts = list()
    for page in page_lines:
        abstract = get_abstract(page)
        if abstract:
            abstracts.append(abstract)
    return abstracts


def pdf_serializer(pdf: PDF) -> List[str]:
    content = list()
    for page in pdf:
        lines = list()
        line = str()
        for char in page:
            if char == "\n":
                # EOL
                line = line.strip()
                lines.append(line)
                line = str()
            else:
                line += char
        content.append(lines)
    return content


if __name__ == "__main__":
    doc_paths = get_document_paths()
    years = _get_years()
    for doc_path, year in zip(doc_paths, years):
        pdf = get_document(doc_path)
        # save_to_json(pdf_serializer(pdf), Path(".") / "data" / "articles" /
        #              f"{year}" / "articles.json")
        abstracts = extract_abstracts(pdf)
        save_to_json(abstracts, Path(".") / "data" /
                     "abstracts" / f"{year} abstracts.json")
