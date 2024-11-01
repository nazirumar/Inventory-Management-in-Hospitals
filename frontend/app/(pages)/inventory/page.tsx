"use client"
import React, { useEffect, useState } from 'react';

import { getInventoryItems } from '@/services/api'; // Adjust the import path as needed



const InventoryPage = () => {
  const [inventoryItems, setInventoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInventoryItems = async () => {
      try {
        const data = await getInventoryItems();
        setInventoryItems(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch inventory items.');
      } finally {
        setLoading(false);
      }
    };

    fetchInventoryItems();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }
  
  return (
    <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
    <div className="flex flex-wrap justify-between gap-3 p-4"><p className="text-[#111517] tracking-light text-[32px] font-bold leading-tight min-w-72">Inventory</p></div>
    <h2 className="text-[#111517] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Low Stock</h2>
    <div className="px-4 py-3 @container">
      <div className="flex overflow-hidden rounded-xl border border-[#dce1e5] bg-white">
        <table className="flex-1">
          <thead>
            <tr className="bg-white">
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-120 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Product Name
              </th>
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-240 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">SKU</th>
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-360 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Category
              </th>
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-480 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Sub-Category
              </th>
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-600 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Current Stock
              </th>
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-720 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Reorder Threshold
              </th>
              <th className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-840 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Supplier
              </th>
            </tr>
          </thead>
          <tbody>
            {inventoryItems.map(item =>(
                <tr key={item.id} className="border-t border-t-[#dce1e5]">
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                  {item.name}
                </td>
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                  SKU# 12345
                </td>
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal"> {item.category}</td>
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Gloves</td>
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">25</td>
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">50</td>
                <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Medline</td>
                </tr>
            ))}
           
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                3M N95 Mask
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 23456
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Masks</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">40</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">100</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">3M</td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Alcohol Wipes
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 34567
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Wipes</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">20</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">30</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Amazon Business
              </td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Thermometers
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 45678
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Thermometer
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">10</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">20</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Cardinal Health
              </td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Hand Sanitizer
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 56789
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Sanitizer
              </td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">30</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">50</td>
              <td className="table-7c01f76d-d343-4714-b449-710c5a588ba8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Henry Schein
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
    </div>
    <h2 className="text-[#111517] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Automatic Reorder Alerts</h2>
    <div className="px-4 py-3 @container">
      <div className="flex overflow-hidden rounded-xl border border-[#dce1e5] bg-white">
        <table className="flex-1">
          <thead>
            <tr className="bg-white">
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-120 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Product Name
              </th>
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-240 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">SKU</th>
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-360 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Category
              </th>
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-480 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Sub-Category
              </th>
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-600 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Current Stock
              </th>
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-720 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Reorder Threshold
              </th>
              <th className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-840 px-4 py-3 text-left text-[#111517] w-[400px] text-sm font-medium leading-normal">
                Supplier
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Face Shields
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 67890
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Shields</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">15</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">20</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">McKesson</td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Isolation Gowns
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 78901
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Gowns</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">25</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">30</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Henry Schein
              </td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Pulse Oximeter
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 89012
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Oximeter</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">10</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">15</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Cardinal Health
              </td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Surgical Masks
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 90123
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Masks</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">35</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">40</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Medline</td>
            </tr>
            <tr className="border-t border-t-[#dce1e5]">
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-120 h-[72px] px-4 py-2 w-[400px] text-[#111517] text-sm font-normal leading-normal">
                Disinfectant Spray
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-240 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                SKU# 01234
              </td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-360 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">PPE</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-480 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">Spray</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-600 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">20</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-720 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">25</td>
              <td className="table-6e59f421-6e20-4ffc-b6f9-745680d47fd8-column-840 h-[72px] px-4 py-2 w-[400px] text-[#647987] text-sm font-normal leading-normal">
                Amazon Business
              </td>
            </tr>
          </tbody>
        </table>
      </div>
     
    </div>
  </div>
  )
}

export default InventoryPage