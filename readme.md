# Render Wt Pt Proj

Code to project 3D keypoints on a model to 2D keypoints on a render of the object. This can be further broken down into two steps:

1) Rendering the 3D object with a given pose with depth map.

2) Projecting the 3D keypoints to the 3D keypoints and pruning of points based on depth.

3) Example Utility of this: Computing optical-flow-like-disparity for 3D models. 

# But Why?

I was using this in my research work, and felt that this might be a good,generalizable tool that others can use as well!

# Acknowledgements

I would like to thank:

* RenderForCNN

* Blender

* x and y for depth map.
