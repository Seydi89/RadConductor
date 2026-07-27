from radconductor.domain.models import DicomSeriesMetadata


def select_ct_series(
    series: list[DicomSeriesMetadata],
) -> DicomSeriesMetadata:
    """
    Select the CT series to be processed.

    Current heuristic:
    choose the CT series with the largest number of slices.
    """

    ct_series = [
        item
        for item in series
        if item.modality.upper() == "CT"
        and item.slice_count > 1
    ]

    if not ct_series:
        raise ValueError("No usable CT series found.")

    selected_series = max(
        ct_series,
        key=lambda item: item.slice_count,
    )

    return selected_series