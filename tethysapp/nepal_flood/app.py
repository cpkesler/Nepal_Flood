from tethys_sdk.base import TethysAppBase, url_map_maker


class NepalFloodMapViewer(TethysAppBase):
    """
    Tethys app class for Nepal Flood Map Viewer.
    """

    name = 'Nepal Flood Map Viewer'
    index = 'nepal_flood:home'
    icon = 'nepal_flood/images/np.jpg'
    package = 'nepal_flood'
    root_url = 'nepal-flood'
    color = '#27afc4'
    description = 'Place a brief description of your app here.'
    enable_feedback = False
    feedback_emails = []
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='nepal-flood',
                           controller='nepal_flood.controllers.home'),
                    UrlMap(name='animation',
                           url='animation',
                           controller='nepal_flood.controllers.animation')
        )
        return url_maps