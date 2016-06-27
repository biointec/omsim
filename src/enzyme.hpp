#ifndef ENZYME_HPP
#define ENZYME_HPP

#include "wx.hpp"

struct enzyme {
        wxString id;
        wxString pattern;
        wxString label;
        wxString fn;
        wxString fp;
        
        enzyme(){}
        enzyme(wxString id_, wxString pattern_, wxString label_, wxString fn_, wxString fp_)
              : id(id_), pattern(pattern_), label(label_), fn(fn_), fp(fp_) {}
};

#endif
