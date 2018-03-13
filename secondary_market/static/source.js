function myFunction(isbuy = true) {
    // Declare variables
    var input, filter, ul, li, a, i;
    if (isbuy) {

        input = document.getElementById('myBuyInput');
        filter = input.value.toUpperCase();
        ul = document.getElementById("myBuyUL");

    }
    else
    {
        input = document.getElementById('mySellInput');
        filter = input.value.toUpperCase();
        ul = document.getElementById("mySellUL");
    }

    li = ul.getElementsByClassName('listitemcontainer');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByClassName("selllistitem")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function validate(obj)
{
  if(!obj.checkValidity())
  {
    obj.style.borderBottomColor = "red";
  }
  else
      {
          obj.style.borderBottomColor =obj.style.borderTopColor ;
      }

}

function matchFVPrice()
{

    isStuGov = document.getElementById('isStuGov');
    warning = document.getElementById('warning');

    if(isStuGov.checked){

        FV = document.getElementById('FV');
        px = document.getElementById('px');

        px.disabled = true;
        px.value = FV.value;

        warning.style.display = ""

    }
    else
    {
        px.disabled = false;
        warning.style.display = "none"
    }

}

function enforceStuGov()
{

    var e = document.getElementById("offereditem");
    var isStuGov = e.options[e.selectedIndex].getAttribute('isStuGov');
    var FV = e.options[e.selectedIndex].getAttribute('FV');
    warning = document.getElementById('warning2');

    if(isStuGov=="True")
    {
        document.getElementById("px_offer").value = FV;
        document.getElementById("px_offer").disabled = true;
        warning.style.display = "";
    }
    else
        {

            warning.style.display = "none";
            document.getElementById("px_offer").disabled = false;
        }



}