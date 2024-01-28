console.log("[ScriptName] VirtualAlloc.js")

var VirtualAlloc = Module.getExportByName(null, "VirtualAlloc");
send("API <VirtualAlloc> attach:" + VirtualAlloc)

Interceptor.attach(VirtualAlloc, {
    onEnter: function(args)
    {
		var api_args = {
			'size':args[1].toInt32(),
			'flNewProtect':args[3]
		}
		var msg = {
			'api_name':'VirtualAlloc',
			'typ:':'args',
			'content':api_args
		}
		send(msg)
	  
	},
	onLeave: function(retval)
	{
    }
});