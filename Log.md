# 运行记录
conda create -n BloodVessel python=3.9(不加python则会导致该虚拟环境中初始没有pip导致后续使用pip会将指定包安装到base环境中，不指定版本会导致python版本过高和torch版本不适配) 
activate BloodVessel  
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 
cd NnunetBloodVessel  
pip install -e .    
pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git  
# idea
使用git开发  
参照Dataset120_RoadSegmentation按2D数据训练看看效果    
因为BloodVessel中test数据集数量过少，所以使用kidney2（另一个供体的肾脏整体作为test）  
要先设置nnUNet_raw、nnUNet_preprocessed、nnUNet_results文件夹和相应的环境变量，为了方便也放在项目根目录外面  
临时环境变量设置方法：  
set nnUNet_raw=F:\DATA\NnunetBloodVessel\nnUNet_raw
set nnUNet_preprocessed=F:\DATA\NnunetBloodVessel\nnUNet_preprocessed
set nnUNet_results=F:\DATA\NnunetBloodVessel\nnUNet_results
# date_log
## 12.5周二
文件名命名为“Dataset001_BloodVessel_2D”。  
为了使用Dataset120_RoadSegmentation预处理流程，要给每个肾脏内数据加前缀，建立temporary临时存放文件夹。预预处理文件为pre_Dataset001_BloodVessel_2D.py    
将环境变量设置到了pycharm中。添加到项目根目录中的环境变量无法在子文件中使用，改为在运行当前文件中修改配置环境变量，成功。
使用Dataset120_RoadSegmentation模板，但是该文件为三通道，所以计算images.sum(2)将三通道压缩为二通道要取消，同时生成json文件部分通道数量修改。  
Dataset001_BloodVessel_2D.py运行成功  