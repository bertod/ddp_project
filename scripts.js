function myFunction(divId) {
  var x = document.getElementById(divId);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function readMore(dotsid, moreid, mybtnid) {
  //var dots = document.getElementById("dots");
  var dots = document.getElementById(dotsid);
  //var moreText = document.getElementById("more");
  var moreText = document.getElementById(moreid);
  //var btnText = document.getElementById("myBtn");
  var btnText = document.getElementById(mybtnid);

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "load more"; 
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "load less"; 
    moreText.style.display = "inline";
  }
}