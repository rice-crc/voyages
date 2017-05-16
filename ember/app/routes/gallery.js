import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    // will load from database via a model in the future
    var gallery = [{
        src: '/assets/images/manuscripts/1.jpg',
        w: 400,
        h: 639,
        title: 'Register of Africans from the Schooner ""Fabiana""',
        msrc: 'The Schooner ""Fabiana"" was captured at sea by British cruisers and adjudicated at a court established at Sierra Leone under international anti-slave trade treaties. The image is of a picture of the first page of the court’s register of ""Liberated Africans"" taken from the ""Fabiana"". The register was kept as a formal record of emancipation that helped protect the individual from subsequent re-enslavement. The image is reproduced courtesy of the British National Archives.'
      },
      {
        src: '/assets/images/manuscripts/2.jpg',
        w: 400,
        h: 545,
        title: 'Register of Africans from the Schooner ""NS de Regla""',
        msrc: 'The Schooner ""NS de Regla"" was captured at sea by British cruisers and adjudicated at a court established at Sierra Leone under international anti-slave trade treaties. The image is of a picture of the first page of the court’s register of ""Liberated Africans"" taken from the ""NS de Regla"". The register was kept as a formal record of emancipation that helped protect the individual from subsequent re-enslavement. The image is reproduced courtesy of the British National Archives.'
      },
      {
        src: '/assets/images/manuscripts/1.jpg',
        w: 400,
        h: 639,
        title: 'Register of Africans from the Schooner ""Fabiana""',
        msrc: 'The Schooner ""Fabiana"" was captured at sea by British cruisers and adjudicated at a court established at Sierra Leone under international anti-slave trade treaties. The image is of a picture of the first page of the court’s register of ""Liberated Africans"" taken from the ""Fabiana"". The register was kept as a formal record of emancipation that helped protect the individual from subsequent re-enslavement. The image is reproduced courtesy of the British National Archives.'
      },
      {
        src: '/assets/images/manuscripts/2.jpg',
        w: 400,
        h: 545,
        title: 'Register of Africans from the Schooner ""NS de Regla""',
        msrc: 'The Schooner ""NS de Regla"" was captured at sea by British cruisers and adjudicated at a court established at Sierra Leone under international anti-slave trade treaties. The image is of a picture of the first page of the court’s register of ""Liberated Africans"" taken from the ""NS de Regla"". The register was kept as a formal record of emancipation that helped protect the individual from subsequent re-enslavement. The image is reproduced courtesy of the British National Archives.'
      }
    ]

    return gallery;
  }

});
