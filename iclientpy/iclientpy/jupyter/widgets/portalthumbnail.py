from ipywidgets import DOMWidget, HTML
from iclientpy.rest.api.model import ViewerMap
from traitlets import Unicode
from string import Template


class PortalThumbnail(DOMWidget):
    thumnail = Unicode('').tag(sync=True)
    title = Unicode('').tag(sync=True)
    description = Unicode('').tag(sync=True)

    def __init__(self, viewerMap: ViewerMap, **kwargs):
        self.viewerMap = viewerMap
        super(PortalThumbnail, self).__init__(**kwargs)

    def _ipython_display_(self, **kwargs):
        html_temp = Template('''
            <table>
                <tr> 
                    <td>
                        <img src="$thumbnail"> 
                    </td> 
                    <td> 
                        <p>title:$title</p>
                        <p>id:$id</p>
                        <p>description:$description</p>
                    </td>
                </tr>
            </table>
        ''')

        html_widget = HTML(value=html_temp.substitute(self.viewerMap.__dict__))
        html_widget._ipython_display_(**kwargs)
