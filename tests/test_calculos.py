import unittest

from core.offgrid_sizing import DEFAULT_LOADS, calculate_offgrid_sizing
from core.ongrid_sizing import calculate_ongrid_sizing
from core.pv_curve_model import calculate_pv_curve


class CalculosSolaresTest(unittest.TestCase):
    def test_arreglo_conectado_a_red_redondea_y_comprueba_area(self):
        result = calculate_ongrid_sizing(
            monthly_consumption_kwh=300,
            coverage=0.8,
            peak_sun_hours=4.5,
            system_losses=0.2,
            panel_power_w=550,
            available_area_m2=12,
            panel_area_m2=2.6,
            energy_rate_cop_kwh=900,
        )
        self.assertEqual(result["panel_count"], 5)
        self.assertAlmostEqual(result["area_required_m2"], 13)
        self.assertFalse(result["fits_available_area"])

    def test_cargas_de_ejemplo_y_autonomia(self):
        result = calculate_offgrid_sizing(
            loads=DEFAULT_LOADS,
            autonomy_days=2,
            bank_voltage=24,
            depth_of_discharge=0.5,
            inverter_efficiency=0.9,
            controller_efficiency=0.95,
            peak_sun_hours=4.5,
            panel_power=550,
            battery_capacity_ah=200,
            desired_inverter_power=1500,
        )
        self.assertAlmostEqual(result["daily_consumption_wh"], 1150)
        self.assertEqual(result["panel_count"], 1)
        self.assertEqual(result["battery_count"], 2)
        self.assertNotIn("Wh/día", DEFAULT_LOADS)

    def test_sin_irradiancia_no_hay_potencia(self):
        result = calculate_pv_curve(0, 25, 49.5, 13.9, 41.7, 13.2, -0.14)
        self.assertEqual(result["pmax"], 0)
        self.assertEqual(result["isc"], 0)


if __name__ == "__main__":
    unittest.main()
