#include "AdvancedPanel.hpp"
#include "TagPanel.hpp"

#include <wx/scrolwin.h>


AdvancedPanel::AdvancedPanel(wxWindow *parent, wxWindowID id, configuration &c_)
      : wxPanel(parent, id), c(c_)
{
        wxBoxSizer *mainbox = new wxBoxSizer(wxHORIZONTAL);
        
        /*
                ctrl box
        */
        wxScrolledWindow *scrollbox = new wxScrolledWindow(this, wxID_ANY);
        
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        
        TagPanel *name = new TagPanel(scrollbox, vbox, "name", c.name, "name");
        TagPanel *prefix = new TagPanel(scrollbox, vbox, "prefix", c.prefix, "prefix");
        /*bool circular;*/
        TagPanel *coverage = new TagPanel(scrollbox, vbox, "coverage", c.coverage, "coverage");
        TagPanel *chips = new TagPanel(scrollbox, vbox, "chips", c.chips, "chips");
        TagPanel *scans_per_chip = new TagPanel(scrollbox, vbox, "scans_per_chip", c.scans_per_chip, "scans_per_chip");
        TagPanel *scan_size = new TagPanel(scrollbox, vbox, "scan_size", c.scan_size, "scan_size");
        TagPanel *avg_mol_len = new TagPanel(scrollbox, vbox, "avg_mol_len", c.avg_mol_len, "avg_mol_len");
        TagPanel *sd_mol_len = new TagPanel(scrollbox, vbox, "sd_mol_len", c.sd_mol_len, "sd_mol_len");
        TagPanel *fragile_correction = new TagPanel(scrollbox, vbox, "fragile_correction", c.fragile_correction, "fragile_correction");
        TagPanel *min_mol_len = new TagPanel(scrollbox, vbox, "min_mol_len", c.min_mol_len, "min_mol_len");
        TagPanel *max_mol_len = new TagPanel(scrollbox, vbox, "max_mol_len", c.max_mol_len, "max_mol_len");
        TagPanel *min_nicks = new TagPanel(scrollbox, vbox, "min_nicks", c.min_nicks, "min_nicks");
        TagPanel *label_snr_filter_type = new TagPanel(scrollbox, vbox, "label_snr_filter_type", c.label_snr_filter_type, "label_snr_filter_type");
        TagPanel *min_label_SNR = new TagPanel(scrollbox, vbox, "min_label_SNR", c.min_label_SNR, "min_label_SNR");
        TagPanel *nick_sd = new TagPanel(scrollbox, vbox, "nick_sd", c.nick_sd, "nick_sd");
        TagPanel *fragile_same = new TagPanel(scrollbox, vbox, "fragile_same", c.fragile_same, "fragile_same");
        TagPanel *fragile_opposite = new TagPanel(scrollbox, vbox, "fragile_opposite", c.fragile_opposite, "fragile_opposite");
        TagPanel *fragile_treshold = new TagPanel(scrollbox, vbox, "fragile_treshold", c.fragile_treshold, "fragile_treshold");
        TagPanel *fragile_factor = new TagPanel(scrollbox, vbox, "fragile_factor", c.fragile_factor, "fragile_factor");
        TagPanel *label_mu = new TagPanel(scrollbox, vbox, "label_mu", c.label_mu, "label_mu");
        TagPanel *label_treshold = new TagPanel(scrollbox, vbox, "label_treshold", c.label_treshold, "label_treshold");
        TagPanel *label_factor = new TagPanel(scrollbox, vbox, "label_factor", c.label_factor, "label_factor");
        TagPanel *chimera_rate = new TagPanel(scrollbox, vbox, "chimera_rate", c.chimera_rate, "chimera_rate");
        TagPanel *chimera_mu = new TagPanel(scrollbox, vbox, "chimera_mu", c.chimera_mu, "chimera_mu");
        TagPanel *chimera_sigma = new TagPanel(scrollbox, vbox, "chimera_sigma", c.chimera_sigma, "chimera_sigma");
        TagPanel *stretch_factor = new TagPanel(scrollbox, vbox, "stretch_factor", c.stretch_factor, "stretch_factor");
        TagPanel *stretch_chip_sd = new TagPanel(scrollbox, vbox, "stretch_chip_sd", c.stretch_chip_sd, "stretch_chip_sd");
        TagPanel *stretch_scan_sd = new TagPanel(scrollbox, vbox, "stretch_scan_sd", c.stretch_scan_sd, "stretch_scan_sd");
        TagPanel *molecule_AI_mu = new TagPanel(scrollbox, vbox, "molecule_AI_mu", c.molecule_AI_mu, "molecule_AI_mu");
        TagPanel *molecule_AI_sd = new TagPanel(scrollbox, vbox, "molecule_AI_sd", c.molecule_AI_sd, "molecule_AI_sd");
        TagPanel *label_AI_mu = new TagPanel(scrollbox, vbox, "label_AI_mu", c.label_AI_mu, "label_AI_mu");
        TagPanel *label_AI_sd = new TagPanel(scrollbox, vbox, "label_AI_sd", c.label_AI_sd, "label_AI_sd");
        TagPanel *molecule_SNR_mu = new TagPanel(scrollbox, vbox, "molecule_SNR_mu", c.molecule_SNR_mu, "molecule_SNR_mu");
        TagPanel *molecule_SNR_sd = new TagPanel(scrollbox, vbox, "molecule_SNR_sd", c.molecule_SNR_sd, "molecule_SNR_sd");
        TagPanel *sim_batch_size = new TagPanel(scrollbox, vbox, "sim_batch_size", c.sim_batch_size, "sim_batch_size");
        TagPanel *seed = new TagPanel(scrollbox, vbox, "seed", c.seed, "seed");
        TagPanel *enzymeFile = new TagPanel(scrollbox, vbox, "enzymeFile", c.enzymeFile, "enzymeFile");
        
        scrollbox->SetSizerAndFit(vbox);
        scrollbox->FitInside();
        scrollbox->SetScrollRate(5, 5);
        /*
                close box
        */
        wxBoxSizer *closebox = new wxBoxSizer(wxVERTICAL);
        wxButton *ok = new wxButton(this, wxID_OK, wxT("Ok"));
        wxButton *cancel = new wxButton(this, wxID_CANCEL, wxT("Cancel"));
        closebox->Add(ok, 0, wxEXPAND);
        closebox->Add(cancel, 0, wxEXPAND);
        
        mainbox->Add(scrollbox, 0, wxALIGN_CENTER | wxALL, 5);
        mainbox->Add(closebox, 0, wxALIGN_CENTER | wxRIGHT | wxTOP | wxBOTTOM, 5);
        
        SetSizerAndFit(mainbox);
}
