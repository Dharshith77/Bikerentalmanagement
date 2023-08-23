var selectedRow = null

function onFormSubmit() {

        var formData = readFormData();
        if (selectedRow == null)
            insertNewRecord(formData);
        else
            updateRecord(formData);
        resetForm();

}

function readFormData() {
    var formData = {};
    formData["bikename"] = document.getElementById("bikename").value;
    formData["brand"] = document.getElementById("brand").value;
    formData["year"] = document.getElementById("year").value;
    formData["price"] = document.getElementById("price").value;
    formData["description"] = document.getElementById("description").value;
    return formData;
}

function insertNewRecord(data) {
var tbodies = document.getElementsByTagName("tbody")[0];
    var table = document.getElementById("bikeinfo.html/booking").tbodies;
    var newRow = table.insertRow(table.length);
    cell1 = newRow.insertCell(0);
    cell1.innerHTML = data.bikename;
    cell2 = newRow.insertCell(1);
    cell2.innerHTML = data.brand;
    cell3 = newRow.insertCell(2);
    cell3.innerHTML = data.year;
    cell4 = newRow.insertCell(3);
    cell4.innerHTML = data.price;
    cell5 = newRow.insertCell(4);
    cell5.innerHTML = data.description;
    cell5 = newRow.insertCell(5);
    cell5.innerHTML = `<a onClick="onEdit(this)">Edit</a>
                       <a onClick="onDelete(this)">Delete</a>`;
}

function resetForm() {
    document.getElementById("bikename").value = "";
    document.getElementById("brand").value = "";
    document.getElementById("year").value = "";
    document.getElementById("price").value = "";
    document.getElementById("description").value = "";
    selectedRow = null;
}

function onEdit(td) {
    selectedRow = td.parentElement.parentElement;
    document.getElementById("bikename").value = selectedRow.cells[0].innerHTML;
    document.getElementById("brand").value = selectedRow.cells[1].innerHTML;
    document.getElementById("year").value = selectedRow.cells[2].innerHTML;
    document.getElementById("price").value = selectedRow.cells[3].innerHTML;
    document.getElementById("description").value = selectedRow.cells[4].innerHTML;
}

function updateRecord(formData) {
    selectedRow.cells[0].innerHTML = formData.bikename;
    selectedRow.cells[1].innerHTML = formData.brand;
    selectedRow.cells[2].innerHTML = formData.year;
    selectedRow.cells[3].innerHTML = formData.price;
    selectedRow.cells[4].innerHTML = formData.description;
}

function onDelete(td) {
    if (confirm('Are you sure to delete this record ?')) {
        row = td.parentElement.parentElement;
        document.getElementById("booking").deleteRow(row.rowIndex);
        resetForm();
    }
}

