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
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)