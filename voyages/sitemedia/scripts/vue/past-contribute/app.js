// main app
var pastContribute = new Vue({
    el: "#past-contribute",
    delimiters: ["[[", "]]"],
    data: {
        enslaved: {},
    },
    created: function() {
        var params = {
            "search_query": {
              "enslaved_id": [
                AFRICAN_ID,
                AFRICAN_ID
              ]
            },
          };

        axios
            .post('/past/api/search', params)
            .then(function(response) {
                pastContribute.enslaved = response.data.data[0];
                var arrivalDateArray = pastContribute.enslaved.voyage__voyage_dates__first_dis_of_slaves ? pastContribute.enslaved.voyage__voyage_dates__first_dis_of_slaves.split([',']) : '';
                console.log(pastContribute.enslaved);
                console.log(arrivalDateArray);
                var arrivalDate = '';

                if (arrivalDateArray.length == 3) {
                  arrivalDate = arrivalDateArray[2];
                } else if (arrivalDateArray.length == 1) {
                  arrivalDate = arrivalDateArray[0];
                }
                pastContribute.enslaved.voyage_year = arrivalDate;
              return;
            })
            .catch(function(error) {
              return error;
            });
    }
});
