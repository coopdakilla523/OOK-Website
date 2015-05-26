function foo()
{
	var xhr = new XMLHttpRequest();
	var feed = document.getElementById("feed");
	console.log("HEY");
	xhr.addEventListener("loadend", function()
    {
		if (xhr.readyState === 4 && xhr.status === 200)
        {
			var rew = xhr.responseText;
			r = JSON.parse(rew);

            feed.innerHTML = ""
			for (i=0; i<r.length; i++)
            {
			    var header = r[i].header;
			    var ook = r[i].ook;
			    var feed_string = "<div class=posts>" + "<legend>" + header + "</legend>" + ook + " </div>";
			    feed.innerHTML += feed_string;
			}
            console.log(feed.innerHTML);
		}
		if (xhr.readyState === 4)
        {
			setTimeout(foo, 5000);
		}
	});

	xhr.open("GET", "/feed.html");
	xhr.send(null);
}


foo();