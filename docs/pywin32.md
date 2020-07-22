Python3中pywin32中常用代码解释
摘要
本文介绍 Win32 版本的 Microsoft Windows 操作系统提供的桌面窗口、顶层窗口和子窗口，以及它们之间的层级关系；解释了应用程序如何游历窗口结构，如何控制桌面上显示的窗口的样式和外观。

窗口层级
在 Microsoft Windows 图形环境中，用来显示信息的最基本元件是窗口。一个窗口和其它窗口之间的关系包括可见性关系、拥有关系和父/子关系，由 Microsoft Windows 管理这些关系。当创建、销毁或者显示一个窗口时，Windows 要用到这种关系信息。Windows 的窗口管理器控制着一个窗口如何和另一个窗口关联，并把每个窗口的窗口进程信息连接起来形成一张层级表，即 window manager’s list 。

窗口管理器使用每个窗口的进程信息结构中的四个元素来构建窗口管理器列表：

•本窗口子窗口的句柄
•子窗口列表中下一个子窗口的句柄 (本窗口的下一兄弟)
•本窗口父窗口的句柄
•本窗口拥有者的句柄

图1.

在初始化 Windows 的时候创建 desktop window，桌面窗口的大小被调整为可以覆盖整个显示区域。窗口管理器把桌面窗口放在窗口管理器列表的顶层。因此，桌面窗口位于窗口层级的顶层。

窗口层级中下一层的窗口叫做 top-level window。一个窗口只要不是子窗口，就是顶层窗口。顶层窗口没有 WS_CHILD 样式。窗口管理器填写每个顶层窗口的下一窗口句柄，把所有的顶层窗口连成一张链表，然后把此链表的表头存储在桌面窗口的子窗口句柄中。这样就建立了顶层窗口和桌面窗口的联系。这个链表被称为 child window list，因为它连接到一个窗口的子窗口句柄。一张子窗口列表中的所有窗口相互间都是兄弟，因此所有顶层窗口互为兄弟。子窗口列表中各元素的顺序决定了它们的Z序，列表中的第一个在Z序的顶端，列表中的最后一个在Z序的底端。窗口管理器依此Z序决定哪个窗口或窗口的哪个部分可见，哪个窗口或窗口的哪个部分被其它窗口盖住。如果一个窗口A出现在另一个窗口B的下面，那么在子窗口列表中 A 位于 B 之后。

所有顶层窗口也通过自己窗口进程信息的父窗口句柄同桌面窗口连接。顶层窗口通过这种方式和桌面窗口连接，就好像它们是桌面窗口的子窗口一样。在游历父/子关系的技术中，确实可以把顶层窗口当作桌面窗口的子窗口。

顶层窗口在创建时，被窗口管理器放到Z序的顶端，因此整个窗口都是可见的。窗口管理器把这个窗口放到桌面窗口的子窗口列表的顶部。有个扩展样式，WS_EX_TOPMOST，可以控制窗口管理器把最近创建的窗口放到窗口管理器列表的哪个部分。所有不包含 WS_EX_TOPMOST 样式的窗口都被窗口管理器放到包含 WS_EX_TOPMOST 样式的窗口之后。因此所有具有 WS_EX_TOPMOST 样式的窗口总是显示在不具有 WS_EX_TOPMOST 样式的窗口前面。

图2.

另一种类型的关系，可以存在于顶层窗口之间：顶层窗口可以拥有其它顶层窗口、或者被其它顶层窗口拥有。一个被拥有的窗口在Z序上总是高于它的拥有者窗口；在它的拥有者最小化时，它总是被隐藏。但是如果它的拥有者被隐藏，这个被拥有的窗口并不会隐藏。因此，如果窗口A拥有窗口B，窗口B又拥有窗口C，当窗口A最小化时，窗口B将被隐藏，而窗口C保持可见。在调用 CreateWindow（或者 CreateWindowEx）创建窗口的时候，给 hwndParent 参数指定一个窗口句柄，这样就指定了被创建的窗口的拥有者。如果 hwndParent 参数指定的窗口不是顶层窗口，Windows 查找此参数指向的窗口的顶层窗口，将找到的顶层窗口作为拥有者。这个被拥有的窗口创建以后，hwndParent 参数指定的窗口存储在窗口进程信息的父窗口字段；作为拥有者的顶层窗口存储在窗口进程信息的拥有者字段。如果应用程序在创建对话框的时候没有特别声明此对话框要是一个子窗口，Windows 将创建一个被拥有的对话框。

图3.

桌面窗口占据着窗口层级的第一层，顶层窗口位于第二层。Child window，即那些创建时带有 WS_CHILD 样式的窗口，位于所有的其它层级。窗口管理器将子窗口同它们的父窗口连接起来的方式和将顶层窗口和桌面窗口连接起来的方式一样。

图4.

子窗口显示在它们父窗口的客户区。窗口管理器使用子窗口列表中从头到尾的顺序来决定子窗口们的Z序。这和用来决定顶层窗口的Z序的方法是一样的。所有顶层窗口都显示在桌面窗口的客户区，因此，看起来就好像它们是桌面的子窗口。

Win32 中有什么不同？
上面介绍的桌面窗口、顶层窗口、被拥有的窗口及子窗口之间的关系，在 Win32 和 Win16 中是一样的。这保证了 Win32 和 Win16 之间的高度兼容，使用窗口层级的应用程序在这两种环境下都能工作。Win32 和 Win16 有两点不同：安全性，多线程。

Windows NT 向窗口层级中添加了一个新层级：每一个运行 Windows NT 的计算机都有一个被称为 WindowStation object 的对象。这个对象构成了工作站的第一层安全性，所有用户对象的安全性都继承自这个对象。一个窗口站对象可以依次地拥有任意数量的桌面对象。每个桌面对象都是一个桌面窗口，前面介绍过桌面窗口。Windows NT 使用两个桌面：一个用来处理登录屏幕、CTRL+ALT+DEL 屏幕、被锁定的工作站的屏幕、屏幕保护程序；另一个桌面用来处理所有其它。目前，应用程序不能创建或者删除桌面。

Win32 和 Win16 的另一个不同之处是使用多线程。Win16 不支持多线程，所以当应用程序创建一个窗口时，程序员不需要考虑线程。在 Win32 中，只要窗口间存在父/子或者拥有/被拥有关系，创建这些窗口的线程就共享同一个输入队列。程序员必须记住，共享输入队列抵消了使用线程带来的好处——任一时刻只有一个线程能处理消息，另外那些共享输入队列的线程必须等待 GetMessage 或 PeekMessage 的返回。在可能的情况下尽量保证父/子窗口或拥有/被拥有的窗口属于同一个线程。

Win32 定义了两个不在窗口层级内的新的窗口类型：foreground window 和 background window。前景窗口是用户当前正在使用的窗口；所有其它窗口都是背景窗口。正常情况下，程序员应当让用户设定前景窗口，然而 Win32 确实提供了两个函数来处理前景窗口，SetForegroundWindow 和 GetForegroundWindow。

游历窗口管理器列表
应用程序以两种方式游历窗口管理器列表：要么通过窗口管理器获得拥有者、父、子、或下一窗口；要么让 Windows 调用一个应用程序为一个窗口集合提供的回调函数。下列函数游历了窗口管理器列表。

```
EnumChildWindows
应用程序使用此函数让 Windows 调用一个应用程序提供的回调函数，此回调函数作用于指定窗口的每个子窗口。Windows 枚举包括子窗口的子窗口在内的所有子窗口。Windows 不会为在 EnumChildWindows 调用之后、返回之前的这段时间内创建的子窗口调用回调函数。

EnumThreadWindows
应用程序使用此函数让 Windows 调用一个应用程序提供的回调函数，此回调函数作用于指定线程的每个窗口。Windows 枚举线程的所有被拥有的和不被拥有的顶层窗口、子窗口、子窗口的子窗口。Windows 不会为在 EnumThreadWindows 调用之后、返回之前的这段时间内创建的窗口调用回调函数。

EnumWindows
应用程序使用此函数让 Windows 调用一个应用程序提供的回调函数，此回调函数作用于每个顶层窗口。Windows 枚举所有被拥有的和不被拥有的顶层窗口。Windows 不会为在 EnumWindows 调用之后、返回之前的这段时间内创建的顶层窗口调用回调函数。

FindWindow
应用程序使用此函数查找符合指定窗口类和窗口标题的、Z序中的第一个顶层窗口。可以仅指定窗口类，或者仅指定窗口标题，或者都指定，或者都不指定。如果都不指定，FindWindow 函数返回Z序中最高的那个顶层窗口。无法通过 FindWindow 获得Z序中位于第一次找到的窗口之下的窗口。

GetDesktopWindow
此函数返回桌面窗口的句柄。

GetNextWindow
Win16 定义了此函数来完成和 GetWindow （见下）不同的功能。Win32 中并没有实现此函数，只是在 WINUSER.H 头文件中定义了一个宏，用来把对 GetNextWindow 的调用转换成对 GetWindow 的调用。

GetParent
如果指定的窗口有父窗口，此函数返回父窗口句柄。对于子窗口，此函数返回其父窗口句柄；对于顶层窗口，若该窗口被拥有，此函数返回拥有者的句柄。当使用 CreateWindow 或 CreateWindowEx 创建被拥有的窗口时，如果想取得传递给这两个函数的窗口句柄，使用 GetWindowWord(GWW_HWNDPARENT)。如果给 CreateWindow 或 CreateWindowEx 传递的是一个非顶层窗口的句柄，那么通过调用 GetWindowWord(GWW_HWNDPARENT) 取得的窗口句柄和 GetParent 的返回值是不一样的。例如：使用 CreateWindow 或 CreateWindowEx 创建对话框时，给 hwndParent 参数传递了一个子窗口句柄。

GetThreadDesktop
此函数返回指定线程的桌面句柄。

GetTopWindow
此函数返回指定窗口的第一个子窗口。第一个子窗口总是位于指定窗口拥有的Z序的顶部。不指定窗口，即传递 NULL 时，此函数返回位于Z序顶部的顶层窗口。

GetWindow
应用程序使用此函数游历窗口管理器列表。GetWindow 接受两个参数：一个窗口句柄（HWND），一个 fwRel（WORD）。fwRel 指出两个窗口要满足什么样的关系，GetWindow 返回满足条件的另一个窗口的句柄。fwRel 取值如下：

•GW_HWNDNEXT: GetWindow 返回下一兄弟窗口的句柄。用 GW_HWNDNEXT 作参数调用 GetNextWindow 将得到同样的结果。
•GW_HWNDFIRST: GetWindow 返回Z序中顶端的兄弟窗口句柄。这窗口的可见度最高。此调用和 GetTopWindow 调用结果相同。
•GW_HWNDLAST: GetWindow 返回Z序中底端的兄弟窗口句柄。这窗口的可见度最低。
•GW_HWNDPREV: GetWindow 返回上一兄弟窗口的句柄。用 GW_HWNDPREV 作参数调用 GetNextWindow 将得到同样的结果。
•GW_OWNER: GetWindow 返回拥有者的句柄。如果没有拥有者，返回 NULL。
•GW_CHILD: GetWindow 返回第一个子窗口的句柄。第一个子窗口位于指定窗口拥有的Z序的顶部。如果没有子窗口，返回 NULL。
IsChild
IsChild 接受两个窗口句柄作参数：hWndParent 和 hWnd。当 hWnd 是 hWndParent 的子、孙、后代时，返回 TRUE。如果从 hWnd 的的父窗口一层一层向上查找，这当中发现了 hWndParent，就说 hWnd 是 hWndParent 的后代。当 hWnd 和 hWndParent 相同时，返回 FALSE。

窗口样式
当应用程序使用 CreateWindow 或 CreateWindowEx 函数创建窗口时，需要通过 dwStyle 参数给窗口指定一些样式属性。样式属性决定了窗口的类型、功能和初始状态。Win32 没有添加、修改或删除原来的样式，Win32 样式和 Win16 样式一模一样。

决定窗口类型的样式
WS_OVERLAPPED
层叠式窗口是顶层窗口，连接到桌面窗口的子窗口列表。应用程序通常使用层叠式窗口作为它们的主窗口。层叠式窗口一定包含一个标题栏，无论是否指定 WS_CAPTION。由于它一定包含一个标题栏，所以它也一定包含一个边框。下面的 WS_CAPTION 部分中有更多关于边框样式的内容。层叠式窗口可以拥有别的顶层窗口、可以被别的顶层窗口拥有、或者同时满足这两种情况。所有层叠式窗口，无论是否指定 WS_CLIPSIBLINGS，都具有此样式。

 

Windows 可以决定层叠式窗口的初始大小和位置。如果要让 Windows 这么做，应用程序使用 CW_USEDEFAULT 作为 CreateWindow 或 CreateWindowEx 的 X 参数的实参。如果应用程序使用 CW_USEDEFAULT 指定层叠式窗口的位置，并且使用 WS_VISIBLE 样式来让窗口一被创建就显示出来，那么 Windows 就会使用 CreateWindow 或 CreateWindowEx 的 Y 参数调用ShowWindow。因此，当一个应用程序将 CW_USEDEFAULT 作为 CreateWindow 或 CreateWindowEx 的 X 参数时，Y 的值必须是下面中的一个：

•SW_HIDE
•SW_SHOWNORMAL
•SW_NORMAL
•SW_SHOWMINIMIZED
•SW_SHOWMAXIMIZED
•SW_MAXIMIZE
•SW_SHOWNOACTIVATE
•SW_SHOW
•SW_MINIMIZE
•SW_SHOWMINNOACTIVE
•SW_SHOWNA
•SW_RESTORE
通常使用 SW_SHOW 作为 Y 参数因为 SW_SHOW 可以让 WS_MAXIMIZE 和 WS_MINIMIZE 样式正确地发挥功能。

 

如果想让 Windows 决定窗口的初始大小，应用程序要把 CreateWindow 或 CreateWindowEx 的 nWidth 参数设为 CW_USEDEFAULT。这时，CreateWindow 或 CreateWindowEx 的 nHeight 参数被忽略。

WS_POPUP
弹出式窗口是顶层窗口，连接到桌面窗口的子窗口列表。弹出式窗口常用于对话框。弹出式窗口和层叠式窗口的主要区别在于弹出式窗口不需要拥有标题栏，而层叠式窗口一定拥有标题栏。弹出式窗口如果没有标题栏，就也可以没有边框。弹出式窗口可以拥有别的顶层窗口、可以被别的顶层窗口拥有、或者同时满足这两种情况。所有弹出式窗口，无论是否指定 WS_CLIPSIBLINGS，都具有此样式。弹出式窗口不能使用 CW_USEDEFAULT 作为位置或大小参数，如果使用，窗口会存在，但是不具有大小，或者不具有位置，或者都不具有。

WS_CHILD
子窗口必须属于一个父窗口，它被限定在这个父窗口的客户区。这是子窗口和层叠式、弹出式窗口的主要区别。子窗口的父窗口既可以是顶层窗口也可以是子窗口。顶层窗口的位置从屏幕的左上角开始计算，子窗口的位置从它们的父窗口的左上角开始计算。子窗口被限制在它们父窗口的客户区，超出的部分被裁剪掉。对话框中的控件是此对话框的子窗口。子窗口不能用 CW_USEDEFAULT 作为位置或大小参数，如果使用，窗口会存在，但是不具有大小，或者不具有位置，或者都不具有。

决定窗口功能和外观的样式
WS_CAPTION
这个样式使得 Windows 在窗口顶部添加一个矩形区域，用来显示文本或标题。层叠式窗口一定包含标题栏。可以在 CreateWindow 或 CreateWindowEx 时指定要显示的文本，也可以调用 SetWindowText 改变文本。包含标题栏的窗口可以包含最大化按钮（WS_MAXIMIZEBOX）、最小化按钮（WS_MINIMIZEBOX）和系统菜单（WS_SYSMENU）。不包含标题栏的窗口，即使包含上面三个样式，Windows 也不会创建它们。

 

不包含标题栏的窗口不能拥有菜单，因为菜单系统依据标题栏来放置菜单。

 

用户可以用鼠标移动具有标题栏的窗口。如果窗口没有标题栏，用户就不能移动它，因为用户必须通过系统菜单移动窗口，而没有标题栏的窗口不具有系统菜单。

 

具有标题栏的窗口要么有一个单线边框，要么有一个较粗的可用来调整窗口大小的边框。如果没有包含 WS_BORDER （单线）和 WS_THICKFRAME （可调整大小）这两个样式中的任何一个，窗口将具有单线边框。WS_CAPTION 实际上是 WS_BORDER 和 WS_DLGFRAME 的组合，WS_CAPTION = WS_BORDER | WS_DLGFRAME，这使得你无法区分具有标题栏、单线边框的窗口和具有标题栏、对话边框的窗口。结果是具有标题栏的窗口无法具有对话框的边框效果，除非使用 WS_EX_DLGMODALFRAME 扩展样式。

WS_MINIMIZEBOX
这个样式使得 Windows 将一个最小化按钮的位图放在窗口右上角。如果窗口有最大化按钮，Windows 把最小化按钮放在最大化按钮的左边。窗口如果没有标题栏就不能有最小化按钮。窗口如果拥有最小化按钮，用户可以通过点击最小化按钮或者通过系统菜单来最小化它；如果不拥有最小化按钮，用户不能最小化它。

WS_MAXIMIZEBOX
这个样式使得 Windows 将一个最大化按钮的位图放在窗口右上角。窗口如果没有标题栏就不能有最大化按钮。窗口如果拥有最大化按钮，用户可以通过点击最大化按钮或者通过系统菜单来最大化它；如果不拥有最大化按钮，用户不能最大化它。

WS_SYSMENU
这个样式使得 Windows 将一个系统菜单的位图放在窗口左上角。系统菜单提供了一个接口，供用户执行下列系统命令：

•还原最小化的窗口
•用键盘移动窗口
•用键盘调整窗口大小
•最小化窗口
•最大化窗口
•关闭窗口
•切换到另一个任务
当窗口拥有系统菜单时，用户可以单击菜单的位图、输入 ALT+SPACEBAR 或者在窗口最小化时单击其图标来展开菜单。如果窗口没有系统菜单，应用程序又没有专门为此提供键盘接口，用户就无法执行系统命令。

 

对于那些最大化以后占据整个屏幕的窗口来说，系统菜单是很重要的。这类窗口如果具有系统菜单，那么在窗口被还原到正常尺寸之前，不能被移动；如果不具有系统菜单，即使它最大化占据了整个屏幕，仍然能够在不还原的情况下移动它。窗口被最大化后，Windows 在系统菜单中禁用移动、调整大小和最大化。因而，具有系统菜单的窗口，最大化以后不能移动；不具有系统菜单的窗口，最大化以后，仍然可以移动。

WS_HSCROLL
这个样式使得 Windows 将一个水平卷动条放在窗口底部。Windows 不会自动卷动窗口的内容。允许水平卷动的窗口必须在自己的窗口过程里处理 WM_HSCROLL 消息，窗口必须在创建时包含 WS_HSCROLL 样式。

WS_VSCROLL
这个样式使得 Windows 将一个垂直卷动条放在窗口右边。Windows 不会自动卷动窗口的内容。允许垂直卷动的窗口必须在自己的窗口过程里处理 WM_VSCROLL 消息，窗口必须在创建时包含 WS_VSCROLL 样式。

WS_BORDER
这个样式使得 Windows 用单线绘制窗口的边框。如果没有指定边框样式，Windows 使用单线绘制所有具有标题栏的窗口。用此样式创建出的窗口不能使用鼠标或键盘来调整大小。

WS_DLGFRAME
这个样式使得 Windows 绘制一个对话框架：一条单线和一条较粗的有颜色的线围绕窗口。这种样式一般指定给一个对话框，但是也可以用在任何没有标题栏的窗口上。仅当指定了WS_EX_DLGMODALFRAME 扩展样式时，具有标题栏的窗口才可以具有此样式。用此样式创建出的窗口不能使用鼠标或键盘来调整大小。

WS_THICKFRAME
这个样式使得 Windows 绘制一个可调整大小的框架：一条较粗的有颜色的线夹在两条单线之间，它们围绕着窗口。此样式常用于应用程序的主窗口。用此样式创建的窗口能够使用鼠标调整大小或者使用键盘通过系统菜单来调整大小。

WS_CLIPCHILDREN
这个样式用于拥有子窗口的窗口，使得 Windows 把子窗口占据的那部分父窗口区域，从父窗口区域中排除。父窗口的绘制不会影响到这部分区域。不包含这个样式时，父窗口的绘制会影响到这部分区域。此样式稍微降低性能，如果应用程序不在窗口上绘制，不要包含此样式。

WS_CLIPSIBLINGS
这个样式使得 Windows 剪取各兄弟窗口之间的客户区域。就是说，兄弟窗口之间不能在彼此的客户区绘制。Windows 对所有顶层窗口（弹出式和层叠式窗口）强制使用此样式。所以顶层窗口不能在其它任何顶层窗口上绘制。默认情况下，Windows 并不剪取兄弟窗口，因此子窗口之间如果存在兄弟关系，它们可以在彼此的窗口上绘制。此样式稍微降低性能，如果兄弟窗口之间无法在彼此的窗口上绘制，不要包含此样式。

决定窗口初始状态的样式
WS_VISIBLE
这个样式使得窗口创建以后马上可见。正常情况下，应用程序必须调用 ShowWindow 函数使窗口可见。

WS_DISABLED
这个样式使得 Windows 创建一个不能使用的窗口。窗口在能被使用之前，无法接受用户输入。应用程序必须提供一个使得窗口能够使用的方法。此样式常用于控件窗口。

WS_MAXIMIZE
这个样式使得 Windows 创建一个最大化的窗口。通过响应 WM_GETMINMAXINFO 消息应用程序可以控制窗口最大化时的尺寸。默认情况下，Windows 把顶层窗口的最大化尺寸设为屏幕尺寸；把子窗口的最大化尺寸设为其父窗口的客户区尺寸。应用程序应该确保 ShowWindow 被调用，以使 WS_MAXIMIZE 样式生效。

WS_MINIMIZE (WS_ICONIC)
这个样式使得 Windows 创建一个最小化的窗口，即，一个图标化的窗口。应用程序应该确保 ShowWindow 被调用，以使 WS_MINIMIZE 样式生效。

窗口标准样式
微软视窗软件开发工具包（sdk）为几种窗口类型提供了一些标准样式。这些样式大多是基本样式的组合。使用这些样式比逐一指定每个单独的样式方便些。

WS_CHILDWINDOW
等同于 WS_CHILD 。一般情况下，创建子窗口时应使用 WS_CLIPSIBLINGS 样式和 WS_CHILD 或 WS_CHILDWINDOW 样式。

WS_OVERLAPPEDWINDOW
等同于 WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX 。应用程序主窗口经常使用此样式。

WS_POPUPWINDOW
等同于 WS_POPUP | WS_BORDER | WS_SYSMENU 。虽然它包含了 WS_SYSMENU 样式，在没有标题栏（WS_CAPTION）的情况下，它不会有系统菜单。

扩展的窗口样式
扩展的窗口样式最早在 3.0 版本的 Windows 中加入。要创建一个具有扩展样式的窗口，应用程序必须使用 CreateWindowEx 函数，不能使用 CreateWindow 函数。

WS_EX_DLGMODALFRAME
这个样式使得 Windows 为具有标题栏的窗口使用对话边框。此样式覆盖 WS_BORDER 和 WS_THICKFRAME 样式，产生一个具有对话框架的窗口。此扩展样式常用于对话框，但任何想使用对话框架的窗口都能使用此样式。

WS_EX_NOPARENTNOTIFY
这个样式是让子窗口使用的。若包含这个样式，Windows 就不向该子窗口的父窗口发送 WM_NOTIFY 消息。默认的情况下，当子窗口被创建或销毁时，Windows 向它的父窗口发送 WM_NOTIFY 消息。

 

从 3.1 版本的 Windows 开始，加入下列扩展的窗口样式。

WS_EX_TOPMOST
这个样式仅用于顶层窗口，子窗口忽略此样式。这个样式使得 Windows 把窗口放在所有不具有 WS_EX_TOPMOST 样式的窗口上面。从 3.1 版本的 Windows 开始，有两类顶层窗口：最顶层的顶层窗口和顶层窗口。最顶层的顶层窗口在Z序上总是位于顶层窗口之上。通过调用 SetWindowPos 函数，给函数传递窗口句柄，给 hwndInsertAfter 参数传递 -1，顶层窗口可以变成最顶层的顶层窗口；通过调用 SetWindowPos 函数，给函数传递窗口句柄，给 hwndInsertAfter 参数传递 1，最顶层的顶层窗口可以变成顶层窗口。

WS_EX_ACCEPTFILES
接受拖放对象的窗口必须包含此样式，Windows 据此来判断一个窗口是否接受对象。若接受，当用户将对象拖过窗口时，Windows 改变拖放时的光标。

WS_EX_TRANSPARENT
这个样式使窗口透明；就是说，窗口下面的任何内容都保持可见，能透过窗口看到它们。但是窗口不会把鼠标或键盘事件也透到下面去。如果它下面的的东西发生变化，窗口将接到绘制消息。透明窗口很适合用来绘制一个位于其它窗口之上的、用于拖动的把手；或者实现一个不需要点击测试的“热点”区域，因为透明的窗口接收了点击消息。
```
