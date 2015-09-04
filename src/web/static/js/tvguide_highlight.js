function channelhighlight(channo) {
    var all = document.getElementsByTagName("tr");
    for (var i = 0; i < all.length; i++)
        {
            if (all[i].id==(channo)) {
                document.getElementById(all[i].id).style.border='#FFBF47';
                document.getElementById(all[i].id).style.borderRadius='7px';
            }
            else if (all[i].id.startsWith('chan')) {
                document.getElementById(all[i].id).style.border='';
                document.getElementById(all[i].id).style.borderRadius='';
            };
        };
}