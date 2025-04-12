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


''' testing character data '''
def example_char_data():
    data = [
        ["Strength", "Defense", "Evasion", "Dexterity", "Recovery", "Intellect",  "Health", "Energy"],
        ("Adan",[[1,2,5,4,3,1, -2,1]]),
        ("Chris", [[4,4,-2,0,-1,3, 3,1]])
    ]
    return data

    
''' Testing example'''
def create_char_graph_example():
    N = 8
    theta = radar_factory(N)

    data = example_char_data()
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(figsize=(9, 4), nrows=1, ncols=2,   
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.45, hspace=0.20, top=0.85, bottom=0.05)
    
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
Creates and displays multiple spider charts of the same number of vars

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

    # figure title
    fig.text(0.5, 0.965, header,
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()

''' Creates and displays spider charts of differing number of vars'''    
def create_multiple_char_spider_types(
    N_lst:list, 
    data_lst:list, 
    labels_lst:list, 
    header:str, 
    colors:list
    ):
    
    # setup radar projection, figure, and temp axes
    theta = radar_factory(N_lst[0])
    
    fig, axs = plt.subplots(figsize=(16, 9), nrows=1, ncols=3,   
                        subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.75, hspace=0.05, top=0.85, bottom=0.05)
    
    ax_inds = range(1, len(axs.flat)+1)
    
    # per unique N spider graph
    for N, (name, case_data), label, color, ax, ind in zip(N_lst, data_lst, labels_lst, colors, axs.flat, ax_inds):
        
        # projection needs to be remade for different N radars
        theta = radar_factory(N)
        
        spoke_labels = label
        
        # remove old ax projection to be replaced
        ax.remove()
        ax = fig.add_subplot(1, 3, ind, projection='radar')

        ax.set_rgrids([-4, -2, 0, 2, 4, 6, 8]) 
        ax.set_rlim(-4, 8)
        ax.set_title(name, weight='bold', size='medium', position=(0.5, 1.1),
                    horizontalalignment='center', verticalalignment='center')
        
        # stats
        ax.plot(theta, case_data, color=color)
        ax.fill(theta, case_data, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)
        
            
    # figure title
    fig.text(0.5, 0.965, header,
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()
