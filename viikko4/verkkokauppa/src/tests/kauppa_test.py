import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 30
            if tuote_id == 3:
                return 0

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, 'karkki', 3)
            if tuote_id == 3:
                return Tuote(3, 'leipä', 7)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                             self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            'pekka', ANY, '12345', ANY, 5)

    def test_kahden_tuotteen_ostosta_otetaan_oikea_summa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            'pekka', ANY, '12345', ANY, 8)

    def test_kahden_saman_tuotteen_ostosta_oikea_summa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            'pekka', ANY, '12345', ANY, 10)

    def test_oikea_summa_lähtee_kun_toista_tuotetta_ei_ole(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            'pekka', ANY, '12345', ANY, 5)

    def test_kauppa_nollaantuu_aloita_asioinnissa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("roosa", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            'roosa', ANY, '11111', ANY, 3)
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_kauppa_pyytää_uuden_viitenumeron_jokaiselle_tapahtumalle(self):
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("roosa", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            'roosa', 1, '11111', ANY, 3)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("roosa", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            'roosa', 2, '11111', ANY, 3)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("roosa", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            'roosa', 3, '11111', ANY, 3)

    def test_poista_korista_toimii(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(2)
        self.kauppa.tilimaksu("roosa", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            'roosa', ANY, '11111', ANY, 5)
