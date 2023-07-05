+++
authors = [
    "Collabora",
]
title = "Debug CODE"
date = "2023-07-04"
home_pos = "4"
description = "How to debug Collabora Online"
tags = [
    "build",
    "make",
]
images = [
    "debug-code.jpg",
]
type = "sidebar"
layout = "sidebar"
+++

You need to enable debugging support to do any practical interactive debugging.

<!--more-->
# Debug CODE
Debug **C**ollabora **O**nline **D**evelopment **E**dition.

Since the steps provided below may vary depending on the platform and tools you are using, it is highly recommended for users to update and adapt the instructions accordingly to suit their specific environment. All are welcome to update this page.


<section id="debug-code" class="debug-code-content">

## Debug in VSCode or VSCodium

If you are trying to debug Collabora online using VSCode then probably first you need add this file in your .vscode code folder.

* [launch.json]({{< ref "/content/snippets/darshan-launch.md" >}})
* Note:
    * Inside launch file make sure url path will be same path as shown in terminal after `make run`.
    * Please replace the variable ${Your-Work-Directory} with your collabora project directory path.

 To Start Debugging :

* Step 1: Do `make run`. 

* Step 2: First put break points in files where you want to see the values or action to be carried out after some events. 

* Step 3: Click on Run and Debug Icon :- You can find this icon in left side of your IDE.
 
* Step 4: Click on document type that you want to open and debug. For an example choose `writer`. It will then launch the document in browser. 

![Run And Debug Option](/images/run-and-debug.png)

* after that you can perform any action. On the bases of your action break point will be hit and you can see the values of variables and code flow in your IDE. like this 

<img src="/images/debug-in-ide.png" alt="Debug In IDE" width="100%">
<br><br>

## Debug in Browser 

Introduction:
Fortunately, modern web browsers come equipped with powerful debugging tools that make this process much more efficient. In this article, we will explore the steps you can follow to debug collabora online code when specific actions are performed.


* Step 1: Open document:
To begin debugging any document first open any document in localhost after `make run`.To build collabora online please refer this blog [Build CODE]({{< relref "build-code.md" >}} "Explore and clone GitHub repository")


* Step 2: Accessing the Developer Tools:
To begin debugging, you first need to access the developer tools in your browser. The exact method varies depending on the browser you are using, but typically, you can right-click on the webpage and select "Inspect" or "Inspect Element." Alternatively, you can use keyboard shortcuts like F12 or Ctrl+Shift+I to open the developer tools.

* Step 3: Navigating to the "Sources" Tab:
Once you have opened the developer tools, you will find a variety of tabs. Look for the "Sources" tab, which is commonly used for debugging JavaScript code. Click on it to proceed.

* Step 4: Identifying the File:
In the "Sources" tab, you will see a list of files associated with the document you are debugging.You can also use `Ctrl+P` to open find source file in which you want to add breakpoint. Locate the JavaScript file you want to debug. If you are unsure which file is responsible for a specific action, you can use browser breakpoints or console logging to narrow down the search.

* Step 5: Setting Breakpoints:
Breakpoints are markers placed in your JavaScript code that pause its execution at a specific line. To set a breakpoint, navigate to the desired line of code within the JavaScript file and click on the line number. This action will set a red marker indicating the breakpoint.

* Step 6: Triggering the Action:
Now, perform the action on the website that you suspect is causing an issue or want to investigate further. It could be clicking a button, submitting a form, or any other action that interacts with the JavaScript code.

* Step 7: Inspecting Variables and Debugging:
When the action is triggered, the execution of the JavaScript code will pause at the set breakpoint. You can now inspect variables, step through the code line by line, and observe the program's state. Use the various debugging controls available, such as stepping over, stepping into, or stepping out of functions, to navigate through the code and understand its flow.

* Step 8: Using Console Logging:
If breakpoints alone are not sufficient for debugging, you can also make use of console logging. Inserting console.log() statements at key points in your JavaScript code allows you to output information to the browser's console. This information can help you track the flow of the program, identify values of variables, and detect any unexpected behavior.

</section>

---

<section id="debug-code-android" class="build-code-content">

</section>

{{< edit-button to="/content/post/debug-code.md" name="Edit page">}}
