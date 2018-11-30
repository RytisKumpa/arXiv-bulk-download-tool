# arXiv-batch-download-tool
arXiv supports batch downloading of the pdf or source files of the academic papers archived. However, the process is not that straightforward. This tool is a one-stop solution written in Python. This solution works on Python3 and needs an AWS account.

Use Instructions:

1. Download and install [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) using pip and set up your authentication creditentials. 
2. Run main.py using command line interface in the location, where you want the files to be downloaded to.
```python main.py```
Folders src and pdf have to already be created in the same location. Manifest file will be downloaded automatically or can be selected locally. Due to the large size of the dataset, this program will download one year worth of academic papers (2018 by default). File format can also be specified - pdf or src (src by default). 
3. To see all arguments use:
```python main.py help```
