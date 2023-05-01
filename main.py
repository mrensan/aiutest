#!/usr/bin/env python
# aiutest

import argparse
import os
import sys

import openai

from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')


def get_completion(prompt, model="gpt-4-0314"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def get_source_code(index_file):
    with open(index_file, "r") as file:
        lines = file.readlines()
    java_classes = ""
    for line in lines:
        line = line.rstrip('\n')
        if line != "":
            with open(line, "r") as file:
                for row in file:
                    if not row.startswith("package") and not row.startswith("import") and row != "\n":
                        java_classes += row
    return java_classes


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your app')

    # Add arguments to parser
    parser.add_argument('-i', '--index', type=str, help='Full path to an index file that includes all source classes full path, each class per line')
    parser.add_argument('-c', '--classname', type=str, help='The desired class name which needs to have unit test')

    # Parse arguments
    args = parser.parse_args()

    if not args.index or not args.classname:
        print("index and classname are mandatory")
        sys.exit(1)

    java_classes = get_source_code(args.index)
    class_name = args.classname

    prompt = f"""
    You are a Java developer assistant. Consider Java classes delimited by triple backticks ```{java_classes}```.
    They are running by Spring Boot. Use junit 5, mockito, assertj technologies to write Unit test for class "{class_name}"
    Consider all the logics in that class and provide different test methods for each scenario. 
    As output: 
    1. only write the Java code without any other description
    2. ignore writing import section to have shorter output
    """

    result = get_completion(prompt)
    print(result)
    

if __name__ == '__main__':
    main()
