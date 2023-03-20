function t(a,r,n){if(a==null)return null;if(typeof a=="string")return{name:"file_data",data:a};if(Array.isArray(a))for(const e of a)t(e,r,n);else a.is_file&&(n==null?a.data="file="+a.name:a.data="proxy="+n+"file="+a.name);return a}export{t as n};
//# sourceMappingURL=utils.83c1ef65.js.map
