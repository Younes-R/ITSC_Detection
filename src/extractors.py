import numpy as np
import pandas as pd


def calc_mean(series: pd.Series):
    return np.mean(series)


def calc_RMS(series: pd.Series | np.ndarray):
    return np.sqrt(np.mean(series * series))


def calc_std(series: pd.Series):
    return np.std(series)


def calc_peak2peak(series: pd.Series | np.ndarray):
    return np.max(series) - np.min(series)


def calc_skewness(series: pd.Series | np.ndarray):
    mean = np.mean(series)
    std = np.std(series)
    z = (series - mean) ** 3  # type: ignore
    z_mean = np.mean(z)
    return z_mean / (std**3)


def calc_kurtosis(series: pd.Series | np.ndarray):
    mean = np.mean(series)
    std = np.std(series)
    z = (series - mean) ** 4  # type: ignore
    z_mean = np.mean(z)
    return z_mean / (std**4)


def calc_CrestFactor(series: pd.Series | np.ndarray):
    abs_max = np.max(np.abs(series))
    RMS = calc_RMS(series)
    return abs_max / RMS


def calc_FormFactor(series: pd.Series | np.ndarray):
    RMS = calc_RMS(series)
    abs_mean = np.mean(np.abs(series))
    return RMS / abs_mean


def calc_ClearenceFactor(series: pd.Series | np.ndarray):
    abs_max = np.max(np.abs(series))
    abs_sqrt_mean = np.mean(np.sqrt(np.abs(series)))
    return abs_max / (abs_sqrt_mean**2)


def calc_ZeroCrossingRate(series: pd.Series | np.ndarray, threshold=1e-6):
    signs = np.zeros_like(series)
    signs[series < threshold] = -1
    signs[series > threshold] = 1

    diff = np.diff(signs)

    return np.count_nonzero(diff) / len(series)


def get_fft_data(series, sampling_rate):
    n = len(series)

    fft_values = np.fft.rfft(series)

    magnitudes = np.abs(fft_values) / (n / 2)

    frequencies = np.fft.rfftfreq(n=n, d=1 / sampling_rate)
    return frequencies, magnitudes


def calc_FundamentalFrequency(frequencies, magnitudes):
    index_max = np.argmax(magnitudes[5:]) + 5
    return frequencies[index_max]


def get_HarmonicMagnitudes(
    frequencies, magnitudes, fund_freq, n_harmonics=7
) -> np.ndarray:
    harmonic_magnitudes = []
    for i in range(1, n_harmonics + 1):
        target_freq = fund_freq * i
        idx = np.argmin(np.abs(frequencies - target_freq))
        harmonic_magnitudes.append(magnitudes[idx])

    return np.array(harmonic_magnitudes)


def get_TotalHarmonicDistortion(harmonic_magnitudes: np.ndarray):
    m1 = harmonic_magnitudes[0]
    higher_harmnonics = harmonic_magnitudes[1:]

    if m1 == 0:
        return 0

    nominator = np.sqrt(np.sum(higher_harmnonics * higher_harmnonics))
    return nominator / m1


def calc_SpectralCentroid(frequencies, magnitudes):
    return np.sum(frequencies * magnitudes) / np.sum(magnitudes)


def calc_SpectralSpread(frequencies, magnitudes):
    spectral_centroid = calc_SpectralCentroid(frequencies, magnitudes)

    nominator = np.sum((frequencies - spectral_centroid) ** 2 * magnitudes)
    denominator = np.sum(magnitudes)

    return np.sqrt(nominator / denominator)


def calc_SidebandRatio(freq, mag, fund_freq):
    left_sideband_mag = mag[(fund_freq - 5 <= freq) & (freq < fund_freq - 0.5)]
    right_sideband_mag = mag[(fund_freq + 0.5 < freq) & (freq <= fund_freq + 5)]

    idx = np.argmin(np.abs(freq - fund_freq))
    fund_mag = mag[idx]

    sideband_energy = (
        np.max(left_sideband_mag) if np.any(left_sideband_mag) else 0
    ) + (np.max(right_sideband_mag) if np.any(right_sideband_mag) else 0)

    return sideband_energy / (2 * fund_mag)


def calc_PhaseImbalance(RMS_a, RMS_b, RMS_c):
    RMS = np.array([RMS_a, RMS_b, RMS_c])
    return (np.max(RMS) - np.min(RMS)) / np.mean(RMS)


def calc_ParkVectorStats(current_a, current_b, current_c):
    current_d = (
        np.sqrt(2 / 3) * current_a
        - (1 / np.sqrt(6)) * current_b
        - (1 / np.sqrt(6)) * current_c
    )
    current_q = (1 / np.sqrt(2)) * current_b - (1 / np.sqrt(2)) * current_c

    magnitudes = np.sqrt(current_d * current_d + current_q * current_q)

    mean = np.mean(magnitudes)
    std = np.std(magnitudes)

    return mean, std


def calc_FluxCurrentPhaseAngle(current_series, flux_series, fund_freq, sampling_rate):
    fft_current = np.fft.rfft(current_series)
    fft_flux = np.fft.rfft(flux_series)

    freqs = np.fft.rfftfreq(len(current_series), 1 / sampling_rate)
    idx = np.argmin(np.abs(freqs - fund_freq))

    phase_current = np.angle(fft_current[idx])
    phase_flux = np.angle(fft_flux[idx])

    angle_diff = phase_current - phase_flux
    angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi

    return angle_diff


def calc_NegativeSequenceCurrent(fft_a, fft_b, fft_c, idx_fund):
    i_a = fft_a[idx_fund]
    i_b = fft_b[idx_fund]
    i_c = fft_c[idx_fund]

    a = np.exp(1j * 2 * np.pi / 3)

    I2_complex = (1 / 3) * (i_a + (a**2) * i_b + (a * i_c))

    return np.abs(I2_complex)


def extract_features_from_csv_file(file_path, SAMPLING_RATE):
    data_sample = pd.read_csv(file_path, skiprows=20)

    mean_a = calc_mean(data_sample["CH1"])
    mean_b = calc_mean(data_sample["CH2"])
    mean_c = calc_mean(data_sample["CH3"])
    mean_flux = calc_mean(data_sample["CH4"])

    rms_a = calc_RMS(data_sample["CH1"])
    rms_b = calc_RMS(data_sample["CH2"])
    rms_c = calc_RMS(data_sample["CH3"])
    rms_flux = calc_RMS(data_sample["CH4"])

    std_a = calc_std(data_sample["CH1"])
    std_b = calc_std(data_sample["CH2"])
    std_c = calc_std(data_sample["CH3"])
    std_flux = calc_std(data_sample["CH4"])

    peak2peak_a = calc_peak2peak(data_sample["CH1"])
    peak2peak_b = calc_peak2peak(data_sample["CH2"])
    peak2peak_c = calc_peak2peak(data_sample["CH3"])
    peak2peak_flux = calc_peak2peak(data_sample["CH4"])

    skewness_a = calc_skewness(data_sample["CH1"])
    skewness_b = calc_skewness(data_sample["CH2"])
    skewness_c = calc_skewness(data_sample["CH3"])
    skewness_flux = calc_skewness(data_sample["CH4"])

    kurtosis_a = calc_kurtosis(data_sample["CH1"])
    kurtosis_b = calc_kurtosis(data_sample["CH2"])
    kurtosis_c = calc_kurtosis(data_sample["CH3"])
    kurtosis_flux = calc_kurtosis(data_sample["CH4"])

    crest_factor_a = calc_CrestFactor(data_sample["CH1"])
    crest_factor_b = calc_CrestFactor(data_sample["CH2"])
    crest_factor_c = calc_CrestFactor(data_sample["CH3"])
    crest_factor_flux = calc_CrestFactor(data_sample["CH4"])

    form_factor_a = calc_FormFactor(data_sample["CH1"])
    form_factor_b = calc_FormFactor(data_sample["CH2"])
    form_factor_c = calc_FormFactor(data_sample["CH3"])
    form_factor_flux = calc_FormFactor(data_sample["CH4"])

    clearence_factor_a = calc_ClearenceFactor(data_sample["CH1"])
    clearence_factor_b = calc_ClearenceFactor(data_sample["CH2"])
    clearence_factor_c = calc_ClearenceFactor(data_sample["CH3"])
    clearence_factor_flux = calc_ClearenceFactor(data_sample["CH4"])

    zcr_a = calc_ZeroCrossingRate(data_sample["CH1"])
    zcr_b = calc_ZeroCrossingRate(data_sample["CH2"])
    zcr_c = calc_ZeroCrossingRate(data_sample["CH3"])
    zcr_flux = calc_ZeroCrossingRate(data_sample["CH4"])

    freq_a, mag_a = get_fft_data(data_sample["CH1"], SAMPLING_RATE)
    fund_freq_a = calc_FundamentalFrequency(freq_a, mag_a)

    harmonic_mags_a = get_HarmonicMagnitudes(freq_a, mag_a, fund_freq_a)
    THD_a = get_TotalHarmonicDistortion(harmonic_mags_a)

    freq_b, mag_b = get_fft_data(data_sample["CH2"], SAMPLING_RATE)
    fund_freq_b = calc_FundamentalFrequency(freq_b, mag_b)

    harmonic_mags_b = get_HarmonicMagnitudes(freq_b, mag_b, fund_freq_b)
    THD_b = get_TotalHarmonicDistortion(harmonic_mags_b)

    freq_c, mag_c = get_fft_data(data_sample["CH3"], SAMPLING_RATE)
    fund_freq_c = calc_FundamentalFrequency(freq_c, mag_c)

    harmonic_mags_c = get_HarmonicMagnitudes(freq_c, mag_c, fund_freq_c)
    THD_c = get_TotalHarmonicDistortion(harmonic_mags_c)

    freq_flux, mag_flux = get_fft_data(data_sample["CH4"], SAMPLING_RATE)
    fund_freq_flux = calc_FundamentalFrequency(freq_flux, mag_flux)

    harmonic_mags_flux = get_HarmonicMagnitudes(freq_flux, mag_flux, fund_freq_flux)
    THD_flux = get_TotalHarmonicDistortion(harmonic_mags_flux)

    spectral_centroid_a = calc_SpectralSpread(freq_a, mag_a)
    spectral_spread_a = calc_SpectralSpread(freq_a, mag_a)
    sideband_ratio_a = calc_SidebandRatio(freq_a, mag_a, fund_freq_a)

    spectral_centroid_b = calc_SpectralSpread(freq_b, mag_b)
    spectral_spread_b = calc_SpectralSpread(freq_b, mag_b)
    sideband_ratio_b = calc_SidebandRatio(freq_b, mag_b, fund_freq_b)

    spectral_centroid_c = calc_SpectralSpread(freq_c, mag_c)
    spectral_spread_c = calc_SpectralSpread(freq_c, mag_c)
    sideband_ratio_c = calc_SidebandRatio(freq_c, mag_c, fund_freq_c)

    spectral_centroid_flux = calc_SpectralSpread(freq_flux, mag_flux)
    spectral_spread_flux = calc_SpectralSpread(freq_flux, mag_flux)

    phase_imbalance = calc_PhaseImbalance(rms_a, rms_b, rms_c)
    park_vector_stats = calc_ParkVectorStats(
        data_sample["CH1"], data_sample["CH2"], data_sample["CH3"]
    )
    flux_current_phase_angle = calc_FluxCurrentPhaseAngle(
        data_sample["CH1"], data_sample["CH4"], fund_freq_a, SAMPLING_RATE
    )
    negative_sequence_current = calc_NegativeSequenceCurrent(
        np.fft.rfft(data_sample["CH1"]),
        np.fft.rfft(data_sample["CH2"]),
        np.fft.rfft(data_sample["CH3"]),
        np.argmin(np.abs(freq_a - fund_freq_a)),
    )

    features_dict = {
        "mean_a": mean_a,
        "mean_b": mean_b,
        "mean_c": mean_c,
        "mean_flux": mean_flux,
        "std_a": std_a,
        "std_b": std_b,
        "std_c": std_c,
        "std_flux": std_flux,
        "rms_a": rms_a,
        "rms_b": rms_b,
        "rms_c": rms_c,
        "rms_flux": rms_flux,
        "peak2peak_a": peak2peak_a,
        "peak2peak_b": peak2peak_b,
        "peak2peak_c": peak2peak_c,
        "peak2peak_flux": peak2peak_flux,
        "skewness_a": skewness_a,
        "skewness_b": skewness_b,
        "skewness_c": skewness_c,
        "skewness_flux": skewness_flux,
        "kurtosis_a": kurtosis_a,
        "kurtosis_b": kurtosis_b,
        "kurtosis_c": kurtosis_c,
        "kurtosis_flux": kurtosis_flux,
        "crest_factor_a": crest_factor_a,
        "crest_factor_b": crest_factor_b,
        "crest_factor_c": crest_factor_c,
        "crest_factor_flux": crest_factor_flux,
        "form_fatcor_a": form_factor_a,
        "form_fatcor_b": form_factor_b,
        "form_fatcor_c": form_factor_c,
        "form_fatcor_flux": form_factor_flux,
        "clearance_factor_a": clearence_factor_a,
        "clearance_factor_b": clearence_factor_b,
        "clearance_factor_c": clearence_factor_c,
        "clearance_factor_flux": clearence_factor_flux,
        "zcr_a": zcr_a,
        "zcr_b": zcr_b,
        "zcr_c": zcr_c,
        "zcr_flux": zcr_flux,
        "harmonic_mag_a_3rd": harmonic_mags_a[2],
        "harmonic_mag_a_5th": harmonic_mags_a[4],
        "harmonic_mag_a_7th": harmonic_mags_a[6],
        "harmonic_mag_b_3rd": harmonic_mags_b[2],
        "harmonic_mag_b_5th": harmonic_mags_b[4],
        "harmonic_mag_b_7th": harmonic_mags_b[6],
        "harmonic_mag_c_3rd": harmonic_mags_c[2],
        "harmonic_mag_c_5th": harmonic_mags_c[4],
        "harmonic_mag_c_7th": harmonic_mags_c[6],
        "harmonic_mag_flux_3rd": harmonic_mags_flux[2],
        "harmonic_mag_flux_5th": harmonic_mags_flux[4],
        "harmonic_mag_flux_7th": harmonic_mags_flux[6],
        "THD_a": THD_a,
        "THD_b": THD_b,
        "THD_c": THD_c,
        "THD_flux": THD_flux,
        "spectral_centroid_a": spectral_centroid_a,
        "spectral_centroid_b": spectral_centroid_b,
        "spectral_centroid_c": spectral_centroid_c,
        "spectral_centroid_flux": spectral_centroid_flux,
        "spectral_spread_a": spectral_spread_a,
        "spectral_spread_b": spectral_spread_b,
        "spectral_spread_c": spectral_spread_c,
        "spectral_spread_flux": spectral_spread_flux,
        "sideband_ratio_a": sideband_ratio_a,
        "sideband_ratio_b": sideband_ratio_b,
        "sideband_ratio_c": sideband_ratio_c,
        "fund_freq": fund_freq_a,
        "phase_imbalance": phase_imbalance,
        "park_vector_mean": park_vector_stats[0],
        "park_vector_std": park_vector_stats[1],
        "flux_current_phase_angle": flux_current_phase_angle,
        "negative_sequence_current": negative_sequence_current,
    }

    return features_dict


if __name__ == "__main__":
    print("Running tests...")
    features_dict = extract_features_from_csv_file(
        "data/raw/0_c2264c30c100.csv", SAMPLING_RATE=10000
    )

    print(len(features_dict))
