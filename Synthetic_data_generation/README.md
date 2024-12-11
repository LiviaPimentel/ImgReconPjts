# Synthetic Data Generation Script in Blender for Machine Learning Object classification

This project provides a Python script designed to generate synthetic data for image recognition tasks using Blender, a powerful 3D graphics software. The script automates rendering multiple images with randomized camera positions, lighting configurations, and object orientations, while also generating corresponding bounding box labels for training computer vision models.

Example of a Blender scene setup for synthetic data generation, showing various objects (triangle, square, cross, and arrow) on a textured plane, with the camera and lighting setup visible.
<img width="717" alt="image" src="https://github.com/user-attachments/assets/3500d3fa-f45e-4c81-a289-12cf4e24a5bd" />

## Why Creating Synthetic Datasets Matter

In the field of machine learning, particularly in computer vision, high-quality datasets are crucial for training accurate models. However, real-world datasets can be challenging to obtain due to privacy concerns, high costs, and limited variability. This is where synthetic datasets come in as a powerful alternative.

### Benefits of Synthetic Datasets

1. **Cost-Effective Data Generation**:
   - Synthetic datasets eliminate the need for manual data collection and labeling, significantly reducing time and costs.

2. **Controlled Environment**:
   - Using tools like Blender, it’s possible to simulate controlled scenarios that may be difficult or dangerous to capture in real life (e.g., industrial inspections or autonomous driving).

3. **Unlimited Data Variability**:
   - Synthetic datasets allow infinite variations in object positions, lighting, and textures, improving model generalization.

4. **Addressing Data Scarcity**:
   - Certain domains, such as healthcare or niche industrial applications, suffer from limited datasets. Synthetic data helps overcome this barrier by simulating realistic data at scale.


## Features

- **Automated Synthetic Data Generation**:
  - Randomizes camera positions and rotations.
  - Varies lighting conditions for better diversity.
  - Exports rendered images with their respective bounding box labels.

- **Bounding Box Calculation**:
  - Detects object visibility in the camera's field of view.
  - Generates bounding box coordinates normalized to the image resolution.
  - Outputs annotations compatible with many object detection frameworks.

- **Flexible Configuration**:
  - Adjustable camera position, rotation ranges, and lighting parameters.
  - Supports rendering images at various resolutions and sample rates.
  - Easy to integrate additional objects or configurations.

## Prerequisites

- **Blender**: Ensure Blender is installed on your system. The script uses Blender's `bpy` module.
- **Python**: The script requires Python 3.x (integrated within Blender).
- **Numpy**: Used for bounding box normalization and processing.

## How It Works

1. **Initialize Objects**: The script loads predefined 3D objects from the Blender scene.
2. **Randomize Scene**: Iterates over different camera locations, rotations, and lighting setups.
3. **Render Images**: Outputs images in PNG format along with bounding box labels in a text file.
4. **Bounding Box Annotation**:
   - Determines the 2D bounding box of objects visible in the camera frame.
   - Writes coordinates in a YOLO-compatible format.

## File Outputs

1. **Images**: Rendered images saved in the specified directory.
2. **Labels**: Text files containing bounding box annotations for each image.
3. **Report**: A progress report file tracking the rendering process.

## Usage

1. **Setup Blender Scene**:
   - Open Blender and prepare your scene with the desired objects, camera, and light.
   - Ensure objects have proper names (e.g., `0`, `1`, `2`, etc.).

2. **Edit Script Parameters**:
   - Update `self.images_filepath` and `self.label_imgs_filepath` with desired output directories.
   - Adjust rendering configurations, such as camera limits, resolution, and sample rates, if necessary.

3. **Run the Script**:
   - Open Blender's scripting workspace.
   - Load this script and press `Run Script`.

4. **Generated Data**:
   - Navigate to the specified directories to find rendered images and label files.

## Key Classes and Functions

- **`Render` Class**:
  - Manages the entire data generation pipeline.
  - Initializes objects, sets camera configurations, and orchestrates rendering.

- **`find_bounding_box(obj)`**:
  - Calculates 2D bounding boxes for objects in the camera's view.

- **`main_rendering_loop(rot_step)`**:
  - Executes the rendering process for all configured positions and rotations.

- **`export_render(res_x, res_y, res_per, samples, file_path, file_name)`**:
  - Configures rendering settings and exports the rendered image to a specified file path.


## Customization

- **Adding New Objects**:
  - Update `self.obj_names` with the new object names in Blender.
- **Changing Render Properties**:
  - Modify `self.camera_z_limits` and rotation limits for diverse perspectives.
  - Adjust `samples` for image quality.

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests for additional features or improvements.

## License

This project is licensed under the MIT License.

---

Start generating high-quality synthetic data for your computer vision projects with this Blender-based pipeline!
