function ReadRinex(fn)
%% ReadRinex  GeoRINEX Python toolbox from Matlab
%
% must first do one-time install in Python from Terminal:
%   pip install -e .
%
% example:
% ReadRinex('tests/data/minimal.10o')

dat = py.georinex.load(fn);

L1 = xarray2mat(dat{'L1'});
sv = xarray2cell(dat, 'sv');

%% plot
figure(1), clf(1)

plot(L1)
xticklabels(sv)
xlabel('SV')
ylabel('pseudorange [m]')
title('L1')
end

function M = xarray2mat(V)
M = double(py.numpy.asfortranarray(V));
end

function C = xarray2cell(V, key)
C = cellfun(@char, cell(V.indexes{key}.values.tolist()), 'uniformoutput', false);
end
