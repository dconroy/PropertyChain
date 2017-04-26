// This is an example object
// Model for Thing object
/*
    {
        "id"             :   String,
        "description"    :   String,
        "year"          :   String.
    }

*/

function Thing(    id,
                   description
               ){

    for (var key in arguments){
        if(arguments[key] == null){
            throw new Error("Incorrect arguments for new Thing.");
        }
    }

    // Attributes for Thing object
    this.id                  =   id;
    this.description         =   description;
    this.date                  =   date;
    this.assoc_id                  =   assoc_id;
    this.apn                  =   apn;
    this.puid                  =   puid;
    this.parcel_id            =parcel_id;
}

var method = Thing.prototype;

// Add a method to the CaseFile prototype
method.example = function(){
    return true;
};

module.exports = Thing;
