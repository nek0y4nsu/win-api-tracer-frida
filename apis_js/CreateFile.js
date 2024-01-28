console.log("[ScriptName] CreateFile.js")

var CreateFileW = Module.getExportByName(null, "CreateFileW");
send("API <CreateFileW> attach:" + CreateFileW)

Interceptor.attach(CreateFileW, {
    onEnter: function(args)
    {
		var api_args = {
			'lpFileName':args[0].readUtf16String(),
			'dwDesiredAccess':args[1]
		}
		var msg = {
			'api_name':'CreateFileW',
			'typ:':'args',
			'content':api_args
		}
		send(msg)
	  
	},
	onLeave: function(retval)
	{
        //console.log("ret var: " + retval)
    }
});