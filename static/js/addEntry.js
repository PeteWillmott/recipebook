var ingredientCounter = 0;
var instructionCounter = 0;


function addEntry(target, destination){
        
        var container = document.getElementById(destination);
        var content = $( "#" + target).val();
        
        if (content) {
                $( "#" + target).val(null);
                
                if (target == "ingredient") {
                        
                        container.append((ingredientCounter + 1) + " " + content + '\n');
                        ingredientCounter++;
                }
                
                else if (target == "instruction") {
                        
                        container.append(instructionCounter + " " + content+ '\n');
                        instructionCounter++;
                        $( "#" + target).attr("placeholder", "Step " + (instructionCounter + 1));
                }
        }
}