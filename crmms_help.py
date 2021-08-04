# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 07:13:01 2020

@author: buriona
"""

import pathlib
from os import path
from shutil import copy
from crmms_utils import get_html_head, get_js_refs


def create_help_page(help_path):
    help_path.replace("/", pathlib.os.sep)
    html_str = f"""
        {get_html_head()}
          <body>
            {get_help_html()}
          </body>
        </html>
        {get_js_refs()}
        """
    with open(path.join(help_path, "help.html"), "w") as html:
        html.write(html_str)
    copy_help_img(help_path)


def get_help_html(html_path="crmms.help"):
    with open(html_path, "r") as html:
        html_str = html.read()
    return html_str


def copy_help_img(help_path, img_path="crmms_help.png"):
    copy(img_path, help_path)


if __name__ == "__main__":

    this_dir = path.dirname(path.realpath(__file__))
    crmms_viz_dir = path.join(this_dir, "crmms_viz")
    create_help_page(crmms_viz_dir.replace("/", "\\"))
    print(f"Created a help page in {crmms_viz_dir}")
