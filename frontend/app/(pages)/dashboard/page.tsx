import React from 'react'

const page = () => {
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
    <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
      <div className="flex flex-wrap justify-between gap-3 p-4">
        <div className="flex min-w-72 flex-col gap-3">
          <p className="text-[#111517] tracking-light text-[32px] font-bold leading-tight">Inventory Dashboard</p>
          <p className="text-[#647987] text-sm font-normal leading-normal">Today, July 15</p>
        </div>
      </div>
      <div className="pb-3">
        <div className="flex border-b border-[#dce1e5] px-4 gap-8">
          <a className="flex flex-col items-center justify-center border-b-[3px] border-b-[#111517] text-[#111517] pb-[13px] pt-4" href="#">
            <p className="text-[#111517] text-sm font-bold leading-normal tracking-[0.015em]">Overview</p>
          </a>
          <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-[#647987] pb-[13px] pt-4" href="#">
            <p className="text-[#647987] text-sm font-bold leading-normal tracking-[0.015em]">Shortages</p>
          </a>
          <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-[#647987] pb-[13px] pt-4" href="#">
            <p className="text-[#647987] text-sm font-bold leading-normal tracking-[0.015em]">Predictions</p>
          </a>
        </div>
      </div>
      <div className="flex flex-wrap gap-4 p-4">
        <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dce1e5]">
          <p className="text-[#111517] text-base font-medium leading-normal">Total inventory value</p>
          <p className="text-[#111517] tracking-light text-2xl font-bold leading-tight">$2.5M</p>
        </div>
        <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dce1e5]">
          <p className="text-[#111517] text-base font-medium leading-normal">Inventory value at risk</p>
          <p className="text-[#111517] tracking-light text-2xl font-bold leading-tight">$1.2M</p>
        </div>
        <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 border border-[#dce1e5]">
          <p className="text-[#111517] text-base font-medium leading-normal">Inventory value in shortage</p>
          <p className="text-[#111517] tracking-light text-2xl font-bold leading-tight">$300K</p>
        </div>
      </div>
      <h3 className="text-[#111517] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Usage rate</h3>
      <div className="flex flex-wrap gap-4 px-4 py-6">
        <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-xl border border-[#dce1e5] p-6">
          <p className="text-[#111517] text-base font-medium leading-normal">Usage rate</p>
          <p className="text-[#111517] tracking-light text-[32px] font-bold leading-tight truncate">$1.5M</p>
          <p className="text-[#647987] text-base font-normal leading-normal">May 2023 - May 2024</p>
          <div className="flex min-h-[180px] flex-1 flex-col gap-8 py-4">
            <svg width="100%" height="148" viewBox="-3 0 478 150" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
              <path
                d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25V149H326.769H0V109Z"
                fill="url(#paint0_linear_1131_5935)"
              ></path>
              <path
                d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25"
                stroke="#647987"
                strokeWidth="3"
                strokeLinecap="round"
              ></path>
              <defs>
                <linearGradient id="paint0_linear_1131_5935" x1="236" y1="1" x2="236" y2="149" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#f0f3f4"></stop>
                  <stop offset="1" stopColor="#f0f3f4" stopOpacity="0"></stop>
                </linearGradient>
              </defs>
            </svg>
            <div className="flex justify-around">
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Jun 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Jul 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Aug 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Sep 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Oct 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Nov 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Dec 2023</p>
            </div>
          </div>
        </div>
      </div>
      <h3 className="text-[#111517] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Shortage prediction</h3>
      <div className="flex flex-wrap gap-4 px-4 py-6">
        <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-xl border border-[#dce1e5] p-6">
          <p className="text-[#111517] text-base font-medium leading-normal">Inventory value</p>
          <p className="text-[#111517] tracking-light text-[32px] font-bold leading-tight truncate">$1.5M</p>
          <p className="text-[#647987] text-base font-normal leading-normal">May 2023 - May 2024</p>
          <div className="flex min-h-[180px] flex-1 flex-col gap-8 py-4">
            <svg width="100%" height="148" viewBox="-3 0 478 150" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
              <path
                d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25V149H326.769H0V109Z"
                fill="url(#paint0_linear_1131_5935)"
              ></path>
              <path
                d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25"
                stroke="#647987"
                strokeWidth="3"
                strokeLinecap="round"
              ></path>
              <defs>
                <linearGradient id="paint0_linear_1131_5935" x1="236" y1="1" x2="236" y2="149" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#f0f3f4"></stop>
                  <stop offset="1" stopColor="#f0f3f4" stopOpacity="0"></stop>
                </linearGradient>
              </defs>
            </svg>
            <div className="flex justify-around">
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Jun 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Jul 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Aug 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Sep 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Oct 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Nov 2023</p>
              <p className="text-[#647987] text-[13px] font-bold leading-normal tracking-[0.015em]">Dec 2023</p>
            </div>
          </div>
        </div>
      </div>
      <h3 className="text-[#111517] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Recommendations</h3>
      <div className="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2">
      <div
      className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg size-14"
      style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/2d687a45-6ada-48c4-90cb-e2fea74a305d.png")' }}
    ></div>
        <div className="flex flex-col justify-center">
          <p className="text-[#111517] text-base font-medium leading-normal line-clamp-1">Order 100,000 units of IV solutions</p>
          <p className="text-[#647987] text-sm font-normal leading-normal line-clamp-2">Current stock: 200,000</p>
        </div>
      </div>
      <div className="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2">
        <div
          className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg size-14"
          style={{backgroundImage: 'url("https://cdn.usegalileo.ai/stability/46d6288e-aeaa-4ad0-9d85-ed12848da7e0.png")'}}
        ></div>
        <div className="flex flex-col justify-center">
          <p className="text-[#111517] text-base font-medium leading-normal line-clamp-1">Order 5,000 units of antibiotics</p>
          <p className="text-[#647987] text-sm font-normal leading-normal line-clamp-2">Current stock: 10,000</p>
        </div>
      </div>
    </div>
  </div>
  )
}

export default page