import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getAssets } from '../services/api';
import { Loader2 } from 'lucide-react';

const AssetSelector = ({ selectedSymbol, onSymbolChange }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['assets'],
    queryFn: getAssets,
  });

  if (isLoading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-4">
          <Loader2 className="h-6 w-6 animate-spin text-primary-600" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-red-50 border border-red-200">
        <p className="text-sm text-red-600">Failed to load assets</p>
      </div>
    );
  }

  // Group assets by category
  const groupedAssets = data?.assets?.reduce((acc, asset) => {
    if (!acc[asset.category]) {
      acc[asset.category] = [];
    }
    acc[asset.category].push(asset);
    return acc;
  }, {});

  const categoryLabels = {
    forex: '💱 Forex',
    commodity: '🥇 Commodities',
    us_bond: '🇺🇸 US Bonds',
    cn_bond: '🇨🇳 China Bonds',
    us_index: '📈 US Indexes',
    cn_index: '📊 China Indexes',
  };

  return (
    <div className="card">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Select Asset
      </label>
      <select
        value={selectedSymbol}
        onChange={(e) => onSymbolChange(e.target.value)}
        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      >
        {Object.entries(groupedAssets || {}).map(([category, assets]) => (
          <optgroup key={category} label={categoryLabels[category] || category}>
            {assets.map((asset) => (
              <option key={asset.symbol} value={asset.symbol}>
                {asset.name} ({asset.symbol})
              </option>
            ))}
          </optgroup>
        ))}
      </select>
    </div>
  );
};

export default AssetSelector;
