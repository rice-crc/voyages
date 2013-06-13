from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command
from .models import Glossary

@override_settings(LANGUAGE_CODE='en')
class GlossaryTest(TestCase):
    fixtures = ['glossary_tests.json']
    initial_objects = 0

    def setUp(self):
        self.initial_objects = Glossary.objects.count()

    def test_initial_view(self):
        # Check number of objects:
        self.assertGreater(Glossary.objects.count(), 0)


        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)

        # Check first entry
        first = Glossary.objects.get(pk=1)
        self.assertEqual(first.term, "Abolition")
        self.assertEqual(first.description, "Government-led initiatives to end the legal trade in enslaved peoples. France abolished its slave trade in 1794, but re-instituted it legally in 1815. Denmark first abolished permanently its slave trade (1802). Britain spearheaded the international abolition movement, culminating in the termination of the British slave trade (1807) and slavery within the British Empire (1833). The Spanish government ended the slave trade to Cuba in 1867; slavery ended in Cuba in 1886 and then in Brazil in 1888.")

    def test_adding_items(self):
        # Add two test items
        added1 = Glossary.objects.create(term="Albariv", description="His explen prougg tring thience Barce, haffer). Tyr go, inguin the Empros they\ onta de thaill andent. 59. I the edup pagney on ascat of sure con be admist pro nes quisel rof stvore lign a or ace dratic morn welancu prorva un he Ferite In thess.\ (hissel sce-so prelle Cardth ogy bistu lionle appost, a be san ung andarm nesatis quis 10, poned poutio sm, exis anin Diatro.")
        added2 = Glossary.objects.create(term="Wgsfew", description="Homarro palium was ques: R. Effic fros ru nonamba soccom men unater par? Norespo better logorr finfacco pope lecurg enctut slue a and fillupo han hinke crair callet Taktur komer ulansli not iftem al bentra vo of musill I co sught, the waresca empoin inve forne zen ing colood beta, jetted, ca. Thear: Howert, frat a diguar un my resat Gal by of of ince so by sis unt, hed tion potte der avio Cammen war themen Estrun Scough, Golund a vince cou mation zinens parde coltach ceriet weepavo by dest no ilentre jole exter able it wells.' by comman otress eitiop obsevid le go de vion witabio prigor ing ens, thatia, aticaro anclu pre, kon Con to Manconi an ithe undes con catris gese deffils und a ocand inte in stuare der's the sur des. Jano. Capand ing a lectra parnit cultha utiona say rearom 12. 36.")

        # Check number of objects
        self.assertEqual(Glossary.objects.count(), self.initial_objects + 2)

        # Check added items
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+1).term, "Albariv")
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+1).description, "His explen prougg tring thience Barce, haffer). Tyr go, inguin the Empros they\ onta de thaill andent. 59. I the edup pagney on ascat of sure con be admist pro nes quisel rof stvore lign a or ace dratic morn welancu prorva un he Ferite In thess.\ (hissel sce-so prelle Cardth ogy bistu lionle appost, a be san ung andarm nesatis quis 10, poned poutio sm, exis anin Diatro.")
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+2).term, "Wgsfew")
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+2).description, "Homarro palium was ques: R. Effic fros ru nonamba soccom men unater par? Norespo better logorr finfacco pope lecurg enctut slue a and fillupo han hinke crair callet Taktur komer ulansli not iftem al bentra vo of musill I co sught, the waresca empoin inve forne zen ing colood beta, jetted, ca. Thear: Howert, frat a diguar un my resat Gal by of of ince so by sis unt, hed tion potte der avio Cammen war themen Estrun Scough, Golund a vince cou mation zinens parde coltach ceriet weepavo by dest no ilentre jole exter able it wells.' by comman otress eitiop obsevid le go de vion witabio prigor ing ens, thatia, aticaro anclu pre, kon Con to Manconi an ithe undes con catris gese deffils und a ocand inte in stuare der's the sur des. Jano. Capand ing a lectra parnit cultha utiona say rearom 12. 36.")

        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)
