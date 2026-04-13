import pytest

pytest.importorskip("matplotlib")
matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")

from scripts.evaluation.generate_figures import (
    FIG4_METHOD_ORDER,
    FIG_ATTACK_STRATEGIES,
    build_fig2_ratio_dataframe,
    build_fig4a_logp_matrix,
    build_fig4b_effect_matrix,
    create_fig4a_figure,
    remove_demoted_fig5_outputs,
)


def test_fig2_ratio_dataframe_uses_two_methods_with_four_ratios():
    df = build_fig2_ratio_dataframe()

    assert sorted(df["Method"].unique().tolist()) == ["GIF", "GNNDelete"]
    assert sorted(df["Ratio"].unique().tolist()) == [0.01, 0.05, 0.1, 0.2]
    assert sorted(df["Strategy"].unique().tolist()) == ["hybrid_v4", "im_v4", "random", "tracin"]

    counts = (
        df.groupby(["Method", "Ratio", "Strategy"])["Seed"]
        .nunique()
        .reset_index(name="n_seeds")
    )
    assert not counts.empty
    assert counts["n_seeds"].min() >= 4

    random_rows = df[df["Strategy"] == "random"]
    assert not random_rows.empty
    assert random_rows["Relative_F1_Drop"].mean() > 1.0

    gnn_im = df[(df["Method"] == "GNNDelete") & (df["Strategy"] == "im_v4")]
    assert gnn_im["Relative_F1_Drop"].mean() > 12.0

    gif_random = df[(df["Method"] == "GIF") & (df["Strategy"] == "random")]
    assert gif_random["Relative_F1_Drop"].mean() < 2.0


def test_fig4a_logp_matrix_has_expected_shape_and_support_levels():
    matrix = build_fig4a_logp_matrix()

    assert matrix.index.tolist() == FIG4_METHOD_ORDER
    assert matrix.columns.tolist() == FIG_ATTACK_STRATEGIES
    assert matrix.shape == (5, 3)

    assert matrix.loc["GIF", "TracIn"] > 1.3
    assert matrix.loc["IDEA", "IM"] > 1.0
    assert matrix.loc["MEGU", "IM"] < 1.0


def test_fig4b_effect_matrix_matches_fig4a_layout_and_signs():
    matrix = build_fig4b_effect_matrix()

    assert matrix.index.tolist() == FIG4_METHOD_ORDER
    assert matrix.columns.tolist() == FIG_ATTACK_STRATEGIES
    assert matrix.shape == (5, 3)

    assert matrix.loc["GNNDelete", "IM"] > 6.0
    assert matrix.loc["GraphEraser", "IM"] > 3.0
    assert matrix.loc["MEGU", "TracIn"] < 0.0


def test_fig4a_uses_plot_legend_instead_of_overlapping_colorbar_text():
    fig, ax, cbar = create_fig4a_figure()

    legend = ax.get_legend()
    assert legend is not None
    legend_texts = [text.get_text() for text in legend.get_texts()]
    assert "p < 0.05" in legend_texts
    assert "0.05 <= p < 0.10" in legend_texts
    assert "p >= 0.10" in legend_texts

    assert len(cbar.ax.texts) == 0
    plt = pytest.importorskip("matplotlib.pyplot")
    plt.close(fig)


def test_remove_demoted_fig5_outputs_is_available():
    assert callable(remove_demoted_fig5_outputs)
