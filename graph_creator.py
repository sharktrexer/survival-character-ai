import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def radar_factory(num_vars):
    """
    Create a radar chart with `num_vars` Axes. 
    From https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    """
    frame = 'polygon'
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    
    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def example_data():
    '''
    Example of data format
    data = [
        [Stat names],
        (Character name, [
            [stat values],
            [another set of stat values to display on same spider chart],
            [etc],
            ]),
        ]
    '''
    data = [
        ['Sulfate', 'Nitrate', 'EC', 'OC1', 'OC2', 'OC3', 'OP', 'CO', 'O3'],
        ('Basecase', [
            [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00],
            [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00],
            [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00],
            [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00],
            [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00]]),
        ('With CO', [
            [0.88, 0.02, 0.02, 0.02, 0.00, 0.05, 0.00, 0.05, 0.00],
            [0.08, 0.94, 0.04, 0.02, 0.00, 0.01, 0.12, 0.04, 0.00],
            [0.01, 0.01, 0.79, 0.10, 0.00, 0.05, 0.00, 0.31, 0.00],
            [0.00, 0.02, 0.03, 0.38, 0.31, 0.31, 0.00, 0.59, 0.00],
            [0.02, 0.02, 0.11, 0.47, 0.69, 0.58, 0.88, 0.00, 0.00]]),
        ('With O3', [
            [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03],
            [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00],
            [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00],
            [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95],
            [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]]),
        ('CO & O3', [
            [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01],
            [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00],
            [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00],
            [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88],
            [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]])
    ]
    return data

def example_char_data():
    data = [
        ["Strength", "Defense", "Evasion", "Dexterity", "Recovery", "Intellect",  "Health", "Energy"],
        ("Adan",[[1,2,5,4,3,1, -2,1]]),
        ("Chris", [[4,4,-2,0,-1,3, 3,1]])
    ]
    return data

''' Matplotlib provided example'''
def create_example_charts():
    N = 9                  # Number of axes,
    theta = radar_factory(N)

    data = example_data()
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,   
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate Axes
    # loop goes over ever "character"
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])                     # change to -4, to 8 in steps of 2
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        # loop goes over every set of stats
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    legend = axs[0, 0].legend(labels, loc=(0.9, .95),
                              labelspacing=0.1, fontsize='small')

    # title
    fig.text(0.5, 0.965, '5-Factor Solution Profiles Across Four Scenarios',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()
    
def create_char_graph_example():
    N = 8
    theta = radar_factory(N)

    data = example_char_data()
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(figsize=(9, 4), nrows=1, ncols=2,   
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.45, hspace=0.20, top=0.85, bottom=0.05)
    
    colors = ['b', 'r', 'g', 'm', 'y']
    color = 'r'
    # Plot the four cases from the example data on separate Axes
    # loop goes over ever "character"
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([-4, -2, 0, 2, 4, 6, 8]) 
        ax.set_rlim(-4, 8)
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        # loop goes over every set of stats
        for d in case_data:
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    #labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    #legend = axs[0, 0].legend(labels, loc=(0.9, .95),labelspacing=0.1, fontsize='small')

    # title
    fig.text(0.5, 0.965, 'Physical Stats of the Lovers',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()
    
#create_char_graph_example()

'''
Example of data format
    data = [
        (Character name, [stat values]),
        (Character name, [stat values]),
        etc
        ]
'''
def create_char_graph(N, data, labels, header, color='r'):
    
    theta = radar_factory(N)

    spoke_labels = labels

    fig, axs = plt.subplots(figsize=(16, 9), nrows=2, ncols=5,   
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.75, hspace=0.05, top=0.85, bottom=0.05)
    
    # Plot each case of character data on separate spider charts
    # loop goes over ever "character"
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([-4, -2, 0, 2, 4, 6, 8]) 
        ax.set_rlim(-4, 8)
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        
        # stats
        ax.plot(theta, case_data, color=color)
        ax.fill(theta, case_data, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    #labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    #legend = axs[0, 0].legend(labels, loc=(0.9, .95),labelspacing=0.1, fontsize='small')

    # title
    fig.text(0.5, 0.965, header,
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()
    
def create_multiple_spider_types(N_lst:list, data_lst:list, labels_lst:list, header:str, colors:list):
    
    theta = radar_factory(N_lst[0])

    spoke_labels = labels_lst[0]
    
    fig = plt.subplots(figsize=(16, 9), nrows=1, ncols=3,   
                        subplot_kw=dict(projection='radar'))
    fig[0].subplots_adjust(wspace=0.75, hspace=0.05, top=0.85, bottom=0.05)
    
    # per unique N spider graph
    for N, (name, case_data), label, color, ax in zip(N_lst, data_lst, labels_lst, colors, fig[1]):
        
        theta = radar_factory(N)
        
        spoke_labels = label
        
        ax = plt.subplots(nrows=1, ncols=1,   
                        subplot_kw=dict(projection='radar'))

        ax.set_rgrids([-4, -2, 0, 2, 4, 6, 8]) 
        ax.set_rlim(-4, 8)
        ax.set_title(name, weight='bold', size='medium', position=(0.5, 1.1),
                    horizontalalignment='center', verticalalignment='center')
        
        # stats
        ax.plot(theta, case_data, color=color)
        ax.fill(theta, case_data, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)
            
    # title
    fig.text(0.5, 0.965, header,
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()


    