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

#### Virtual environment setup for Conda\Windows
Using beautah channel

```cmd
conda env create --prefix=<"c:\path\adjacent\to\crmms_plots\crmm_py"> beautah/crmm_py
```

conversely...

[<img src"https://anaconda.org/beautah/crmm_py/badges/installer/env.svg">](https://anaconda.org/beautah/crmm_py/2021.04.05.155535/download/crmm_py.yml)

```cmd
conda create --prefix=<"c:\path\adjacent\to\crmms_plots\crmm_py"> --file=<"c:\path\to\file\downloaded\above\crmm_py.yml">
```

or simply use the ./setup/crmm_py.yml. Important to note use of prefix to same dir crmms_plot is located in, crmms_viz_run_all.py assumes windows systems will use conda with a prefix in that location.

```cmd
conda create --prefix=<"c:\path\adjacent\to\crmms_plots"> --file=<"c:\path\to\crmms_plots\setup\crmm_py.yml">
```

#### Virtual environment setup for Linux\venv

```bash
python3 -m venv /path/adjacent/to/crmms_plots/crmm_py
cd /path/adjacent/to/crmms_plots/crmm_py
source ./bin/activate
pip install --file --requirement /path/to/crmms_plots/setup/requirements.txt

```

The general idea here is to set up a conda env (on windows) or venv (on linux) that "lives" next to the crmms_plots repo, otherwise you'll need to adjust the .bat or .sh files to suit

## Install hdb_api repo inside crmms_plots

```bash
cd /path/to/crmms_plots
git clone https://github.com/beautah/hdb_api.git
```
make sure to add an hdb_config.json (see [hdb_api readme.md](https://github.com/beautah/hdb_api/blob/master/README.md))

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