# CRMMS (MTOM/24MS) Visualization Toolset

Visualization tools for MTOM and 24MS output data

## Environment setup

The following libraries are required for the project

- [> python3.7](https://www.python.org/downloads/)
- [pandas](https://pandas.pydata.org/)
- [plotly](https://plot.ly/)
- [requests](https://2.python-requests.org/en/master/)
- [hdb_api](https://github.com/beautah/hdb_api)
- [folium](https://github.com/python-visualization/folium)

## Usage

```bash
# for single run
python ./crmms_viz_gen.py --config_path </path/to/config/crmms_viz.config> --output </path/to/static/file/server> --config <config_key>

# to run all keys in a config file
python ./crmms_viz_run_all.py --config </path/to/config/crmms_viz.config> --output </path/to/static/file/server>
```

## Contributing
Contact [Beau Uriona](mailto:beau.uriona@gmail.com)

## License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Public Disclaimer:
The programs, projects, code-bases, and files (FILES) hosted on this site are provided by developers located within different USBR offices and may not necessarily be officially endorsed, developed, or published by USBR. Unless otherwise specified, FILES as originally published constitutes works of the United States Government and are not subject to domestic copyright protection under 17 USC ¤ 105. Subsequent contributions by members of the public, however, retain their original copyright. FILES are provided "AS IS" without warranty of any kind, express or implied, including but not limited to the warranties of merchantibility, fitness for a particular purpose and noninfringement. In no event shall the authors of the Files be liable for any claim, damages or other liability, whether in an action of contract, torto or otherwise, arising from, out of or in connection with the FILES or the use or other dealings in the FILES.

## Note for existing and potential USBR users:
Individual developers (you) are responsible for ensuring that the programs, projects, code-bases, and files (FILES) that are uploaded to GitHub are free of issues and questions pertaining to licensing, shareability, intellectual property, personally indetifiable information, and other potential issues that violates established data sharing, information security, code-of-conduct, and other similar rules and regulations. USBR and the moderators of this organizational account will not be held liable for violations or litigation involving any of the FILES hosted on this site. Send a note to ktarbet and/or jrocha to get added to this group.

The Adapted Privacy Impact Assessment covers use of the free GitHub service so long as all projects and repositories are kept publicly available. DO NOT add projects and repositories that are set to private under this organizational account. Keep your private projects under your own personal GitHub account.