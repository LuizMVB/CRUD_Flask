
var index, table = document.getElementById('table');
for(var i = 1; i < table.rows.length; i++)
{
    table.rows[i].cells[5].onclick = function ()
    {
        index = this.parentElement.rowIndex;
        plate = table.rows[index].cells[2].innerHTML;
        window.location = "rm_car_row/" + plate;
    };
}