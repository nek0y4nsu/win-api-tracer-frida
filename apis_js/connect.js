console.log("[ScriptName] connect.js")

var connect = Module.getExportByName(null, "connect");
send("API <connect> attach:" + connect)

function inet_ntoa(num){
    var nbuffer = new ArrayBuffer(4)
    var ndv = new DataView(nbuffer)
    ndv.setUint32(0, num)
    var a = new Array()
    for(var i = 0; i < 4; i++){
        a[i] = ndv.getUint8(i)
    }
    return a.join('.')
}

function parse_sockaddr(buffer){
	//console.log(buffer)
	var sockaddrDataView = new DataView(buffer);
	var port = sockaddrDataView.getUint16(2).toString()
	var ip_int = sockaddrDataView.getUint32(4)
	var ip_str = inet_ntoa(ip_int)
	return {
		'ip':ip_str,
		'port':port
	}
}


Interceptor.attach(connect, {
    onEnter: function(args)
    {
		
		var target_addr = parse_sockaddr(args[1].readByteArray(16))
		
		var api_args = {
			'ip':target_addr.ip,
			'port':target_addr.port
		}
		
		var msg = {
			'api_name':'connect',
			'typ:':'args',
			'content':api_args
		}
		send(msg)
    },
	
	onLeave: function(retval)
	{
        //send(ret_content)
    }
	
});