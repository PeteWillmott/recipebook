function hideShowPassword() {
  var psswd = document.getElementsByClassName("pwrd");
  for (var i=0; i<psswd.length; i++)
  if (psswd[i].type === "password") {
    psswd[i].type = "text";
  } else {
    psswd[i].type = "password";
  }
}

function adminTabVisability(ident1, ident2, ident3) {
    document.getElementById(ident1).style.display = "block";
    document.getElementById(ident2).style.display = "none";
    document.getElementById(ident3).style.display = "none";
}

var ingredientCounter = 0;
var instructionCounter = 0;


function addEntry(target, destination){
        
        var container = document.getElementById(destination);
        var content = $( "#" + target).val();
        var entry = document.createElement("input");
        var br = document.createElement("br");
        
        $( "#" + target).val(null);
        
        if (target === "ingredient") {
                entry.id = "ingredient" + ingredientCounter;
                entry.name = "ingredient"
                container.append(entry);
                $( "#ingredient" + ingredientCounter).val( content );
               ingredientCounter++;
               container.append(br);
        }
        
        else if (target === "instruction") {
                entry.id = "instruction" + instructionCounter;
                entry.name = "instruction"
                container.append(entry);
                $( "#instruction" + instructionCounter ).val( content );
                container.append(br);
                instructionCounter++;
                $( "#" + target).attr("placeholder", "Step " + (instructionCounter + 1));
        }
    }

function noSubmit(target, destination) {
    if (event.key === "Enter") {
        event.preventDefault();
        addEntry(target, destination);
    }
}
