做一个类似inspect.exe的组件并融入到项目中, 形成自成一体、模式闭环



貌似这种拾取器的问题在于没有形成全链路的索引值, 所以使用起来还是很麻烦



pywinauto.print_control_identifiers() 的问题在于无法在界面形象的看到, 无法进行反推



提出一个疑问: 

python实现的窗口句柄拾取器?

能够和python进行交互的窗口句柄拾取器?



能够且比较方便使用的:

UISpy
ViewWizard 2.63
inspect.exe





使用c#做拾取器

使用pythonnet调动c#并融入到项目中





获取当前鼠标所在位置的控件的位框值和定位索引值

根据位框值进行绘框, 监听CTRL进行确认拾取



原来在浏览器中是如何做拾取器的?

为页面每一个元素添加一个鼠标悬停的事件, 并且监控CTRL键的事件, 进行确认拾取元素



难道win环境下也能这么干?



生成类xpath值 -> 使用类xpath值



使用类xpath值:

封装pywinauto实现使用xpath值找寻控件



生成类xpath值:

