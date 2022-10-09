/* sends a http request to toggle a task's completion status
 *
 * the request should be sent when the checkbox is changed
 *
 * Parameters
 * ----------
 * cb - The checkbox that was changed
*/
function toggle_task(cb)
{
    // grab the task uuid from the checkbox data
    var task_uuid = cb.dataset.uuid;

    // construct the http request
    var url = "api/Task/" + task_uuid + "/update";
    console.log(url);
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {
            //console.log(http.responseText);
            location.reload();
        }
        else if (http.readyState == 4 && http.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request, and set the data type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json");

    // send off the request
    http.send(JSON.stringify({ "complete" : cb.checked }));
}

function archive_engagement(btn, archive="archived")
{
    // grab the task uuid from the checkbox data
    var eng_uuid = btn.dataset.uuid;

    // construct the http request
    var url = "api/Engagement/" + eng_uuid + "/update";
    console.log(url);
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {
            //console.log(http.responseText);
            location.reload();
        }
        else if (http.readyState == 4 && http.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request, and set the data type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json");

    // send off the request
    http.send(JSON.stringify({ "category" : archive }));
}

function edit_engagement(input, model, attribute)
{
    // grab the task uuid from the checkbox data
    var eng_uuid = input.dataset.uuid;

    // construct the http request
    var url = "/api/Engagement/" + eng_uuid + "/update";
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {
            console.log(http.responseText);
            location.reload();
        }
        else if (http.readyState == 4 && http.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request, and set the data type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json");

    // send off the request
    http.send(JSON.stringify({ [attribute] : input.value }));
}