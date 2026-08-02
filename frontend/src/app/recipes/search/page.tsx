'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense, useEffect } from 'react';

function SearchRedirectInner() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString());
    router.push(`/recipes?${params.toString()}`);
  }, [router, searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600" />
    </div>
  );
}

export default function SearchRedirectPage() {
  return (
    <Suspense fallback={null}>
      <SearchRedirectInner />
    </Suspense>
  );
}
