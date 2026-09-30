from html import escape
from os.path import relpath
from pathlib import Path

from radconductor.pipeline.context import PipelineContext


def write_html_report(
    context: PipelineContext,
    output_path: Path,
) -> Path:
    """Write a minimal HTML summary for one completed pipeline run."""

    lines = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>RadConductor Report</title>",
        "<style>",
        "body { font-family: sans-serif; max-width: 900px; margin: 2rem auto; "
        "padding: 0 1rem; color: #222; }",
        "table { border-collapse: collapse; width: 100%; }",
        "th, td { border-bottom: 1px solid #ddd; padding: .6rem; "
        "text-align: left; }",
        "img { max-width: 100%; height: auto; border: 1px solid #ddd; }",
        ".notice { background: #fff4ce; padding: .8rem; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>RadConductor Report</h1>",
        '<p class="notice">Research use only. This report is not a diagnostic '
        "assessment. QC status describes technical checks, not anatomical or "
        "clinical validity.</p>",
        "<h2>Scan</h2>",
        f"<p><strong>Study:</strong> {escape(str(context.study_path))}</p>",
    ]

    if context.selected_series is not None:
        series = context.selected_series
        lines.append(
            "<p><strong>Selected series:</strong> "
            f"{escape(series.series_instance_uid)} "
            f"({escape(series.modality)}, {series.slice_count} slices)</p>"
        )

    if context.volume_metadata is not None:
        metadata = context.volume_metadata
        lines.append(
            "<p><strong>Volume:</strong> "
            f"{escape(str(metadata.size))} voxels; "
            f"spacing {escape(str(metadata.spacing_mm))} mm</p>"
        )

    if context.nifti_path is not None:
        nifti_link = _relative_link(
            target=context.nifti_path,
            report_directory=output_path.parent,
        )
        lines.append(
            f'<p><a href="{escape(nifti_link)}">Generated NIfTI volume</a></p>'
        )

    if context.organ_volumes_ml:
        lines.extend(
            [
                "<h2>Organ measurements</h2>",
                "<table>",
                "<thead><tr><th>Organ</th><th>Volume</th>"
                "<th>QC</th></tr></thead>",
                "<tbody>",
            ]
        )

        for organ, volume_ml in context.organ_volumes_ml.items():
            qc_status = (
                "Technical QC passed"
                if organ in context.qc_passed_organs
                else "Not available"
            )
            lines.append(
                "<tr>"
                f"<td>{escape(organ)}</td>"
                f"<td>{volume_ml:.1f} mL</td>"
                f"<td>{qc_status}</td>"
                "</tr>"
            )

        lines.extend(["</tbody>", "</table>"])

    if context.mask_overlay_paths:
        lines.append("<h2>Segmentation overlays</h2>")

        for organ, overlay_path in context.mask_overlay_paths.items():
            overlay_link = _relative_link(
                target=overlay_path,
                report_directory=output_path.parent,
            )
            lines.extend(
                [
                    f"<h3>{escape(organ)}</h3>",
                    f'<img src="{escape(overlay_link)}" '
                    f'alt="{escape(organ)} segmentation overlay">',
                ]
            )

    if context.merlin_result is not None:
        result = context.merlin_result
        lines.extend(
            [
                "<h2>Merlin phenotype predictions</h2>",
                "<p>Whole-scan research predictions. These are independent "
                "of the selected organ masks.</p>",
                "<ol>",
            ]
        )

        for prediction in result.predictions:
            lines.append(
                "<li>"
                f"{escape(prediction.description)} "
                f"[{escape(prediction.phecode)}] — "
                f"{prediction.probability:.4f}"
                "</li>"
            )

        lines.append("</ol>")

    lines.extend(["</body>", "</html>"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output_path


def _relative_link(
    target: Path,
    report_directory: Path,
) -> str:
    return Path(relpath(target, start=report_directory)).as_posix()
