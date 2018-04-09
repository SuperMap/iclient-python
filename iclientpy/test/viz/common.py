class MockMapView(object):
    fit_bounds = []

    def add_layer(self, layer):
        self.layers = [layer]

    def _ipython_display_(self, **kwargs):
        print('python_display method')
