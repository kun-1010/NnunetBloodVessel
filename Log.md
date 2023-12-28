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
# date_log
## 12.5周二
因为BloodVessel中test数据集数量过少，所以使用kidney2（另一个供体的肾脏整体作为test）    
要先设置nnUNet_raw、nnUNet_preprocessed、nnUNet_results文件夹和相应的环境变量，为了方便也放在项目根目录外面    
临时环境变量设置方法：    
set nnUNet_raw=F:\DATA\NnunetBloodVessel\nnUNet_raw   
set nnUNet_preprocessed=F:\DATA\NnunetBloodVessel\nnUNet_preprocessed   
set nnUNet_results=F:\DATA\NnunetBloodVessel\nnUNet_results   
文件名命名为“Dataset001_BloodVessel_2D”。  
为了使用Dataset120_RoadSegmentation预处理流程，要给每个肾脏内数据加前缀，建立temporary临时存放文件夹。预预处理文件为pre_Dataset001_BloodVessel_2D.py      
将环境变量设置到了pycharm中。添加到项目根目录中的环境变量无法在子文件中使用，改为在运行当前文件中修改配置环境变量，成功。  
`上句方式运行采用右键运行时可用，若使用nnUNetv2_plan_and_preprocess进行预处理，则要在设置->工具->终端->环境变量中设置，则环境变量在终端可见`  
使用Dataset120_RoadSegmentation模板，但是该文件为三通道，所以计算images.sum(2)将三通道压缩为二通道要取消，同时生成json文件部分通道数量修改。    
使用pre_Dataset001_BloodVessel_2D.py给各肾脏数据加前缀并转移到固定文件夹  
使用latter_Dataset001_BloodVessel_2D.py划分训练集和验证集  
`Dataset001_BloodVessel_2D.py运行成功填充nnUNet_raw`  
entry_points.txt中存放的是终端运行命令对应的模块  
nnUNetv2_plan_and_preprocess -d 1 --verify_dataset_integrity
## 12.6周三
autodl上传文件后最最好是tar而不是rar，否则无法用tar命令解压缩  
可以无卡模式启动，便宜  
使用Autodl pandle和百度网盘连接加速文件上传，速度0.5m/s  
`nnUNetv2_train 1 2d 0运行成功,不是完成，而是测试`   
用vscode远程开发，git push到github，本地通过git pull拉取，实现信息交互  
以后使用autodl不能在白天传数据，耗时较长，尽量选在晚上  
为了测试kaggle需要数据集格式，尝试运行  
nnUNetv2_predict -i /home/user/Kaggle/Data/BloodVessel/nnUNet_raw/Dataset001_BloodVessel_2D/imagesTs -o /home/user/Kaggle/Data/BloodVessel/nnUNetv2_predict_output -d 1 -c 2d -chk checkpoint_best.pth -f 0 
evaluate_predictions.py用于评估推理结果，pred和gt对比。  
尝试修改predict_from_data_iterator直接得到RLE编码
AutoDL老是上传中断，改变策略：直接上传
## 12.8周五
经过实验，不论用autodl自带的网页版终端还是vscede远程，上传到20G左右会中断，因为操作在夜间进行，具体原因不知  
改变策略为：使用实验室服务器，或者将生数据进行拆分上传。
使用 tar -xvf  nnUNet_preprocessed.tar -C .解压到指定目录（注意不要忘记-C）  
迁移到实验室  
使用ls ~/.ssh查看得知本机未配置git，以下为git配置命令记录： 
git config --global user.name "kun-1010"  
git config --global user.email "2393956270@qq.com"  
ssh-keygen -t rsa -C "2393956270@qq.com"  
ls ~/.ssh  
cat ~/.ssh/id_rsa.pub  
cd Kaggle  
sudo git clone git@github.com:kun-1010/NnunetBloodVessel.git  
ssh -T git@github.com  
sudo git clone git@github.com:kun-1010/NnunetBloodVessel.git  
cd NnunetBloodVessel  
git status  
为了便于避免在同一份代码上做改动而导致冲突或许可以用“同一台主机上的同一个git账户的不同分支”进行协作？  
## 12.9周六
预处理前的labal和预处理后的label数值不一致，导致肉眼误以为数据处理错误，具体原因参考visual_data.ipynb    
使用tmux，可以断联服务器但是其中的进程不会终止  
tmux new -s <session-name>创建指定名称会话  
tmux attach-session -t <session-name>连接指定会话  
tmux kill-session -t <session-name>结束指定会话  
linux终端设置临时环境变量：  
export nnUNet_raw="/home/user/Kaggle/Data/BloodVessel/nnUNet_raw"  
export nnUNet_preprocessed="nnUNet_preprocessed=/home/user/Kaggle/Data/BloodVessel/nnUNet_preprocessed"  
export nnUNet_results="/home/user/Kaggle/Data/BloodVessel/nnUNet_results"   
## 12.10周日  
kaggle上debug  
## 12.11周一  
kaggle上debug
## 12.14周四   
在Kaggle上太麻烦，转战vscode  
visiual.ipynb中编写了rle编码和submission.csv
