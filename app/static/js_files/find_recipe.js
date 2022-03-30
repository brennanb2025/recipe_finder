const entriesPerRow = 3;
const maxRows = 10;
let rowArrIngredient = [];


function add_ingredient() {
    arrTds = document.getElementsByName("ingredientName");
    var ingredient = document.getElementById("ingredientField").value;
    if(!checkOnEnter(ingredient, arrTds)) {
        document.getElementById("ingredientField").value = ""; //empty input ingredient field
        return;
    }
    var add_here = -1;
    for(var i = 0; i < rowArrIngredient.length; i++) {
        if(rowArrIngredient[i] < entriesPerRow) { //able to be put in this row
            add_here = i;
            break;
        }
    }
    if(add_here === -1) { //no spaces found
        if(rowArrIngredient.length == maxRows) { //no available spaces and max # rows
            alert("Max number of attributes reached");
            return;
        }
        var newTr = document.createElement('tr');
        add_here = rowArrIngredient.length;
        newTr.setAttribute("name", "ingredientTr"+add_here);
        newTr.setAttribute("id", "ingredientTr"+add_here);
        document.getElementById("ingredientTable").appendChild(newTr);
        rowArrIngredient.push(0);
    }

    //create user input text td
    var textCell = document.createElement("td");            //create user input and button remove tds
    textCell.setAttribute("name", "ingredientTd");
    textCell.setAttribute("class", "removableCell");
    ingredientName = document.createElement("input");              //create ingredient input and add to textCell
    ingredientName.value = ingredient;
    ingredientName.setAttribute("name", "ingredientName");
    ingredientName.setAttribute("type", "hidden");
    textCell.appendChild(ingredientName); //for getting the ingredient name back in routes
    textCell.appendChild(document.createTextNode(ingredient));

    //create remove button
    var removeBtnCell = document.createElement("td");
    removeBtnCell.setAttribute("name", "ingredientTdRemove");
    removeBtnCell.setAttribute("class", "removeableBtn");
    var remove = document.createElement("input");
    remove.setAttribute("type", "button");
    remove.setAttribute("name", "removeIngredientBtn");
    remove.setAttribute("class", "removeableBtn");
    remove.value = "X";
    remove.addEventListener('click', removeIngredient, false);
    removeBtnCell.appendChild(remove);

    var divContainer = document.createElement("div");       //create div container
    divContainer.setAttribute("name", "divContainer");
    divContainer.setAttribute("class", "divContainer");
    divContainer.appendChild(textCell);        //add user input and remove button to new tray
    divContainer.appendChild(removeBtnCell);     
    
    var newTr = document.createElement("tr");               //create tray to store user input and remove button 
    newTr.appendChild(divContainer);            //add div to new tray

    var newTable = document.createElement("table");         //create new table
    newTable.appendChild(newTr);                //add new tr to table

    var newTd = document.createElement("td");
    newTd.appendChild(newTable);

    ingredientTray = document.getElementById("ingredientTr" + add_here); //get first available tray
    ingredientTray.appendChild(newTd);          //add table to the ingredient tray
    
    rowArrIngredient[add_here] = rowArrIngredient[add_here]+1; //increment value of this row's index
    document.getElementById("ingredientField").value = ""; //empty input ingredient field
    document.getElementById("num_ingredients").value = (parseInt(document.getElementById("num_ingredients").value)+1).toString();
}

function removeIngredient() {
    cellRemove = this.parentNode.parentNode.parentNode.parentNode.parentNode;
    ingredients = cellRemove.parentNode; //the education tray = this.parent x 5
    ingredients.removeChild(cellRemove);
    document.getElementById("num_ingredients").value = (parseInt(document.getElementById("num_ingredients").value)-1).toString()
    rowArrIngredient[ingredients.rowIndex] = rowArrIngredient[ingredients.rowIndex]-1; //decrement the row index
}


function checkOnEnter(word, arr) {
    if(word === "") {
        alert("Error: empty input.");
        return false;
    }
    for(var i = 0; i < arr.length; i++) {
        if(arr[i].value === word) {
            alert("Error: duplicate entry: " + word);
            return false;
        }
    }
    return true;
}