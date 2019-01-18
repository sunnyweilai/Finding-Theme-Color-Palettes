# Color Quantization and Image processing
## This project consists of 3 main parts:
### 1.	Implement color quantization of the image in 2 color spaces (RGB and CIELab) using 3 different kinds of algorithms:
* [`kmeans`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/kmeans): https://en.wikipedia.org/wiki/K-means_clustering
* [`median-cut`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/median-cut): https://www.cs.tau.ac.il/~dcor/Graphics/cg-slides/color_q.pdf
* [`octree`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/octree): https://en.wikipedia.org/wiki/Octree

### 2.	Visualize the color theme palettes and quantized images 
#### All the color palettes and quantized images are in the `img` folder under each color quantization algorithm folder:
* [color palettes and quantized images using `kmeans`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/kmeans/img)
* [color palettes and quantized images using `median-cut`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/median-cut/img)
* [color palettes and quantized images using `octree`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/octree/img)

### 3.	Complete objective image quality assessment (IQA) of the original image and quantized images in two color spaces (RGB and CIELab) with 4 different methods:
* Gradient Magnitude Similarity Deviation (GMSD): https://arxiv.org/pdf/1308.3052.pdf
* Peak Signal-to-Noise Ratio (PSNR): https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
* Structural Similarity (SSIM): https://en.wikipedia.org/wiki/Structural_similarity
* Visual Information Fidelity (VIF): http://utw10503.utweb.utexas.edu/publications/2005/hrs_vidqual_vpqm2005.pdf <br>
#### All the IQA implementations and results are in the `image_quality_assessment(IQA)` folder under each color quantization algorithm folder:
* [IQA of `kmeans`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/kmeans/image_quality_assessment(IQA))
* [IQA of `median-cut`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/median-cut/image_quality_assessment(IQA))
* [IQA of `octree`](https://gitlab.cas.mcmaster.ca/G-ScalE/Lai_Project/tree/master/color_quantization/octree/image_quality_assessment(IQA))

