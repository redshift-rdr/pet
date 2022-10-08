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

function add_fields()
{
    var container = document.getElementById("tasklist_container");

    /*
        <div class="row mb-1">
            <div class="col-2">
                <label for="template_title" class="form-label">Title</label>
            </div>
            <div class="col-4">
                <input type="text" class="form-control" id="template_title">
            </div>
        </div>
    */

    var new_row = document.createElement("div");
    new_row.classList.add("row", "mb-1");

    var first_col = document.createElement("div");
    first_col.classList.add("col-2");
    var label = document.createElement("label");
    label.classList.add("form-label");
    label.innerHTML = "Tasklist title";
    first_col.appendChild(label);

    var second_col = document.createElement("div");
    second_col.classList.add("col-4");
    var input = document.createElement("input");
    input.type = "text";
    input.classList.add("form-control");
    second_col.appendChild(input);

    new_row.appendChild(first_col);
    new_row.appendChild(second_col);
    container.appendChild(new_row);
}