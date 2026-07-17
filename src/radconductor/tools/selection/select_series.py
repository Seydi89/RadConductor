from radconductor.domain.models import DicomSeriesMetadata


def select_ct_series(
    series: list[DicomSeriesMetadata],
) -> DicomSeriesMetadata:
    ct_series = [
        item
        for item in series
        if item.modality.upper() == "CT"
        and item.slice_count > 1
    ]

    if not ct_series:
        raise ValueError("No usable CT series found.")

    print("WARNING - Multiple CT series found - Returning the one with the most number of slices!")
    return max(
        ct_series,
        key=lambda item: item.slice_count,
    )