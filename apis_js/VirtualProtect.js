console.log("[ScriptName] VirtualProtect.js")

var func_addr = Module.getExportByName(null, "VirtualProtect");
send("API <VirtualProtect> attach:" + func_addr)

Interceptor.attach(func_addr, {
    onEnter: function(args)
    {
		var lpAddress = args[0]
		var api_args = {
			'lpAddress':lpAddress,
			'dwSize':args[1].toInt32(),
			'flNewProtect':args[2]
		}
		//dump address ansi
		var dump = lpAddress.readAnsiString(10)
		
		var msg = {
			'api_name':'VirtualProtect',
			'typ:':'args',
			'content':api_args,
			'dump':dump
		}
		send(msg)
	  
	},
	onLeave: function(retval)
	{
        var msg = {
			'api_name':'VirtualProtect',
			'typ:':'retval',
			'content':retval
		}
		//send(msg)
    }
});